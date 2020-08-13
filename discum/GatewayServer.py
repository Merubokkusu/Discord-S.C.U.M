import websocket
import ssl
from .erlang import *
from .erlang import etfDictToJson,getName #just in case
from .Logger import *

class GatewayServer():
    '''
    Manages authentication and data transfer to/from http://gateway.discord.gg
    '''
    URL = "wss://gateway.discord.gg/?encoding=etf&v=6"

    class OPCODE:
        '''
        Taken from https://discordapp.com/developers/docs/topics/opcodes-and-status-codes#voice-opcodes
        '''
        # Name                  Code    Client Action   Description
        DISPATCH =              0  #    Receive         dispatches an event
        HEARTBEAT =             1  #    Send/Receive    used for ping checking
        IDENTIFY =              2  #    Send            used for client handshake
        STATUS =                3  #    Send            used to update the client status
        VOICE_STATE =           4  #    Send            used to join/move/leave voice channels
        #                       5  #    ???             ???
        RESUME =                6  #    Send            used to resume a closed connection
        RECONNECT =             7  #    Receive         used to tell clients to reconnect to the gateway
        REQUEST_GUILD_MEMBERS = 8  #    Send            used to request guild members
        INVALID_SESSION =       9  #    Receive         used to notify client they have an invalid session id
        HELLO =                 10 #    Receive         sent immediately after connecting, contains heartbeat and server debug information
        HEARTBEAT_ACK =         11 #    Sent immediately following a client heartbeat that was received
        GUILD_SYNC =            12 #    ???             ???

    def __init__(self, proxy_host, proxy_port):
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.__ws = websocket.WebSocket(sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
        self.__session_settings = {}
        self.__ws.settimeout(5)
        
    def Connect(self, token):
        gateway_auth_data = {OtpErlangBinary(str.encode('op'),bits=8): 2,
                OtpErlangBinary(str.encode('d'),bits=8):
                    {OtpErlangBinary(str.encode('properties'),bits=8):
                        {OtpErlangBinary(str.encode('client_version'),bits=8): OtpErlangBinary(str.encode('0.0.305'),bits=8),
                        OtpErlangBinary(str.encode('os'),bits=8): OtpErlangBinary(str.encode('Windows'),bits=8),
                        OtpErlangBinary(str.encode('os_version'),bits=8): OtpErlangBinary(str.encode('6.1.7601'),bits=8),
                        OtpErlangBinary(str.encode('os_arch'),bits=8): OtpErlangBinary(str.encode('x64'),bits=8),
                        OtpErlangBinary(str.encode('release_channel'),bits=8): OtpErlangBinary(str.encode('stable'),bits=8),
                        OtpErlangBinary(str.encode('client_build_number'),bits=8): 44004,
                        OtpErlangBinary(str.encode('browser'),bits=8): OtpErlangBinary(str.encode('Discord Client'),bits=8),
                        OtpErlangBinary(str.encode('client_event_source'),bits=8): OtpErlangAtom('nil')
                        },
                    OtpErlangBinary(str.encode('compress'),bits=8): False,
                    OtpErlangBinary(str.encode('token'),bits=8): OtpErlangBinary(str.encode("{}".format(token)), bits=8),
                    OtpErlangBinary(str.encode('presence'),bits=8):
                        {OtpErlangBinary(str.encode('status'),bits=8): OtpErlangBinary(str.encode('online'),bits=8),
                        OtpErlangBinary(str.encode('since'),bits=8): 0,
                        OtpErlangBinary(str.encode('afk'),bits=8): False,
                        OtpErlangBinary(str.encode('activities'),bits=8): []
                        }
                    }
                }
        # Connect to gateway
        gateway_auth_data = term_to_binary(gateway_auth_data)
        if self.__proxy_host != False and self.__proxy_port != False:
            self.__ws.connect(self.URL, origin="https://discordapp.com", http_proxy_host=self.__proxy_host, http_proxy_port=self.__proxy_port, header={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36"})
        else:
            self.__ws.connect(self.URL, origin="https://discordapp.com", header={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36"})
        Logger.LogMessage('Gateway_wss connecting -> {}'.format(self.URL), log_level=LogLevel.OK)

        # Receive response
        response = str(self.__ws.recv())
        Logger.LogMessage('Gateway_wss received <- {} bytes'.format(len(response)))
        Logger.LogMessage('Gateway_wss data received \r\n', to_file=False, to_console=False, hex_data=response)

        # Send auth message
        Logger.LogMessage('Gateway_wss sending -> {} bytes'.format(len(gateway_auth_data)))
        self.__ws.send_binary(gateway_auth_data)
        Logger.LogMessage('Gateway_wss data sent -> \r\n', to_file=False, to_console=False, hex_data=gateway_auth_data)

        # Receive media_token
        response = self.__ws.recv()
        etf_data = binary_to_term(response)
        Logger.LogMessage('Gateway_wss received <- {} bytes'.format(len(response)))
        Logger.LogMessage('Gateway_wss data received <- \r\n', to_file=False, to_console=False, hex_data=response)
        etfDictToJson(self.__session_settings, etf_data[OtpErlangAtom(str.encode('d'))]) #self.__session_settings has a lot of important data, not to mention free server.members yay
        Logger.LogMessage('Authenticated over gateway as {}'.format(self.__session_settings[str.encode('user')][str.encode('id')]), log_level=LogLevel.OK)
        Logger.LogMessage('Session id: {}'.format(self.__session_settings[str.encode('session_id')].decode("utf-8")))
        
    def return_session_settings():
        return self.__session_settings
