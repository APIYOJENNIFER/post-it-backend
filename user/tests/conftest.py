# import pytest
# from django.conf import settings
# # from rest_framework.test import APIClient

# @pytest.fixture(scope="session")
# def test_db_setup():
#     settings.DATABASE['default'] = {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': 'db',
#         'NAME': 'test_postgres',
#         'USER': 'test',
#         'PASSWORD': 'testuser'
#     }
# # @pytest.fixture(scope="function")
# # def api_client() -> APIClient:
# #     """
# #     Provide APIClient
# #     :return: APIClient
# #     """
# #     yield APIClient()