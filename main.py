from time import time

from modules.scrape import Scraper
from modules.bruter import Bruter
from lib.constants  import BANNER, INORI
from lib.colors     import Colors


if __name__ == '__main__' :
    print(f'\x1bc{BANNER}')
    
    mirai_scraper: object = Scraper()
    print(f'{Colors.WHITE}Scraped {Colors.LIGHTPINK}{len(mirai_scraper.list_ips)} {Colors.WHITE}IP address(s)')
    bruter = Bruter(mirai_scraper.list_ips)
    
    start: int = time()
    print(f'{Colors.WHITE}Executing {INORI}{Colors.WHITE}...\n')
    bruter.run()
    
    print(f'{Colors.WHITE}Found {Colors.LIME}{len(bruter.results)} {Colors.PINKRED}mirai {Colors.WHITE}CNC(s)\n')
    
    '''
    if bruter.results:
        print(bruter.results)
        for result in bruter.results:
            
            print(f"""{Colors.LIME}• {INORI} {Colors.WHITE}has logged in {Colors.PINKRED}{result['ip']} {Colors.WHITE}({Colors.LIGHTPINK}{result['mysql_login']}{Colors.WHITE}) {Colors.WHITE}({Colors.LIGHTPINK}{result['arch']}{Colors.WHITE})""")
            print(f' {Colors.LIGHTPINK}• {Colors.WHITE}Dumping databases...')
            if result['databases']:
                for database in result['databases']:
                    for db, creds in database.items():
                        print(f'   {Colors.PINKRED}• {Colors.LIGHTPINK}{db}{Colors.WHITE}: {Colors.PINKRED}{f"{Colors.WHITE},{Colors.PINKRED} ".join(creds)}')
            else:
                print(f'  {Colors.RED}• {Colors.WHITE}No database found.')
            print() 
    '''
              
    print(f'{Colors.WHITE}Execution speed: {Colors.LIGHTPINK}{str(time() - start).split(".")[0]} {Colors.WHITE}seconds.\n') 