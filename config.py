import os


class BaseConfig(object):
    API_ENDPOINT_FUNNELS = os.environ['API_ENDPOINT_FUNNELS']
    API_ENDPOINT_FUNNELS_ENUMS = os.environ['API_ENDPOINT_FUNNELS_ENUMS']
    API_AUTH_HEADER = os.environ['API_AUTH_HEADER']

    TESTING = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SITE_NAME = os.environ.get("SITE_NAME", "site_name.com")

    @classmethod
    def init_app(cls, app):
        pass


class DevelopmentConfig(BaseConfig):

    @classmethod
    def init_app(cls, app):
        super(DevelopmentConfig, cls).init_app(app)


class TestingConfig(DevelopmentConfig):
    TESTING = True

    @classmethod
    def init_app(cls, app):
        super(TestingConfig, cls).init_app(app)


class ProductionConfig(BaseConfig):

    @classmethod
    def init_app(cls, app):
        super(ProductionConfig, cls).init_app(app)


class EnvironmentName:
    """
    use this class to refer to names of environments.
    """
    development = 'development'
    testing = 'testing'
    production = 'production'
    default = 'default'

    @classmethod
    def all_names(cls):
        return [attr for attr in dir(cls)
                if not (attr.startswith('__') or attr == 'all_names')]


configs = {
    EnvironmentName.development: DevelopmentConfig,
    EnvironmentName.testing: TestingConfig,
    EnvironmentName.production: ProductionConfig,
    EnvironmentName.default: DevelopmentConfig
}
