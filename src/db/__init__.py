from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Create a MetaData instance to hold table definitions
metadata = MetaData()

# Define a base class for declarative class definitions
# This base class maintains a catalog of classes and tables
Base = declarative_base(metadata=metadata)
