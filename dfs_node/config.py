class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    

class DevelopmentConfig(Config):
    MONGO_URL = "Your Mongo DB URL"
    MONGO_DB = "dfs_db"
    LIBRARY_COLL = "library"
    CONFIGS_COLL = "configs"
    DEPLOYMENTS_COLL = "deployments"
    TEMPLATES_COLL = "templates"
    SERVICES_COLL = "services"
    DFS_SERVER = "dfs-server"
    NODE_MANAGER = "node-manager"
    DFS_NODE = "node-agent"
    NODE_MONITOR = "node-monitor"
    DEVELOPMENT = True

class ProductionConfig(Config):
    MONGO_URL = "Your Mongo DB URL"
    MONGO_DB = "dfs_db"
    LIBRARY_COLL = "library"
    CONFIG_COLL = "configs"
    DEPLOYMENT_COLL = "deployments"
    TEMPLATES_COLL = "templates"
    SERVICES_COLL = "services"
    DEVELOPMENT = False
    DEBUG = False
    DFS_SERVER = "dfs-server"
    NODE_MANAGER = "node-manager"
    DFS_NODE = "node-agent"
    NODE_MONITOR = "node-monitor"
    ENV = "production"
