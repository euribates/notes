Amazon Web Services: S3
========================================================================

.. tags:: aws, devops


Cómo saber si existe un fichero en un *bucket*, y su tamaño
------------------------------------------------------------------------

Esto debería funcionar:

.. code:: python

    def file_in_cloud(client, bucket, key):
        response = client.list_objects_v2(Bucket=bucket, Prefix=key)
        for obj in response.get('Contents', []):
            if obj['Key'] == key:
                return True, obj['Size']
        return False, -1
