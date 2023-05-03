class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    

class DevelopmentConfig(Config):
    MONGO_URL = "mongodb+srv://dfs-user:dfssvm2023@dfs-cluster0.qbwo159.mongodb.net/?retryWrites=true&w=majority"
    MONGO_DB = "dfs_db"
    LIBRARY_COLL = "library"
    CONFIGS_COLL = "configs"
    DEPLOYMENTS_COLL = "deployments"
    TEMPLATES_COLL = "templates"
    SERVICES_COLL = "services"
    DFS_SERVER = "dfs-server"
    NODE_MANAGER = "node-manager"
    DFS_NODE = "node-agent"
    DEVELOPMENT = True

class ProductionConfig(Config):
    MONGO_URL = "mongodb+srv://dfs-user:dfssvm2023@dfs-cluster0.qbwo159.mongodb.net/?retryWrites=true&w=majority"
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
    ENV = "production"
