from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from requests import Session
from .service_ops import *
from celery import task

class ServiceInvoker:
    thread_pool_executor_size = 2
    async_session = FuturesSession(executor=ThreadPoolExecutor(max_workers=thread_pool_executor_size))
    sync_session = Session()

    @staticmethod
    @task()
    def get (service_name, operation, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.get(url, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.get(url, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))

    @staticmethod
    @task()
    def options (service_name, operation, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        kwargs.setdefault('allow_redirects', True)

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.options(url, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.options(url, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))

    @staticmethod
    @task()
    def head (service_name, operation, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        kwargs.setdefault('allow_redirects', False)

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.head(url, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.head(url, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))

    @staticmethod
    @task()
    def post (service_name, operation, data=None, json=None, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.post(url, data=data, json=None, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.post(url, data=data, json=None, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))

    @staticmethod
    @task()
    def put (service_name, operation, data=None, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.put(url, data=data, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.put(url, data=data, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))

    @staticmethod
    @task()
    def patch (service_name, operation, data=None, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.patch(url, data=data, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.patch(url, data=data, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))

    @staticmethod
    @task()
    def delete (service_name, operation, **kwargs):
        ep = ServiceOps.get_callable_endpoint(service_name)

        if ep is None:
            raise ServiceDiscoError('No callable endpoint found for %s' % service_name)

        url = ep + operation

        if url is not None:
            try:
                if 'async' in kwargs and kwargs['async'] is True:
                    return ServiceInvoker.async_session.delete(url, **kwargs)
                else:
                    del kwargs['async']
                    return ServiceInvoker.sync_session.delete(url, **kwargs)
            except BaseException as e:
                raise ServiceDiscoError('Call failed : %s' % str(e))
