from django.contrib.gis.db.backends.postgis.base import DatabaseWrapper as PostGisDatabaseWrapper
from django.contrib.gis.db.backends.postgis.schema import PostGISSchemaEditor


class DatabaseWrapper(PostGisDatabaseWrapper):
    SchemaEditorClass = PostGISSchemaEditor
