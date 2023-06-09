import cherrypy
import cherrypy_cors
import logging

from logging import Logger

from .exceptions.controller_not_exposed_exception import ControllerNotExposedException
from .exceptions.server_stopped_exception import ServerStoppedException
from .tools.server import ServerRoutesDispatcher
from .tools.typing import ControllerInstanceType


cherrypy.log.error_log.propagate = False
cherrypy.log.access_log.propagate = False


class Server:

    _log: Logger
    _routes_dispatcher: ServerRoutesDispatcher
    _server_settings: dict

    def __init__(self, root_path: str, host: str, port: int):

        self._log = logging.getLogger(__name__)
        self._routes_dispatcher = ServerRoutesDispatcher()
        self._server_settings = {
            'global': {
                'server.socket_host': host,
                'server.socket_port': port,
                'log.screen': False,
                'log.access_file': '',
                'log.error_file': ''
            },
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': root_path,
                'request.dispatch': self._routes_dispatcher,
                'cors.expose.on': True
            }
        }

    def start(self, testing: bool = False) -> None:

        self._log.info('Starting server...')

        try:

            cherrypy_cors.install()
            cherrypy.config.update(self._server_settings)
            cherrypy.tree.mount(self, '/', self._server_settings)
            cherrypy.engine.signals.subscribe()
            cherrypy.engine.start()
            self._log.info('Server started successfully')

            if not testing:

                cherrypy.engine.block()

        except Exception as exception:

            self._log.error('Stopped server because of exception', extra={'exception': exception})

            raise ServerStoppedException

    def register_controller(self, controller_instance: ControllerInstanceType) -> None:

        self._log.debug(f'Registering controller \'{controller_instance.__class__.__name__}\'...')

        try:

            self._routes_dispatcher.register_controller_instance(controller_instance)

        except ControllerNotExposedException as exception:

            self._log.error(f'Error registering controller \'{controller_instance.__class__.__name__}\'. '
                            f'The controller class was not exposed properly')

            raise exception

    def stop(self) -> None:

        self._log.info('Stopping server...')

        try:

            cherrypy.engine.exit()
            cherrypy.server.stop()
            self._log.info('Server stopped successfully')

        except Exception as exception:

            self._log.error('Server stopping failed because of exception', extra={'exception': exception})
