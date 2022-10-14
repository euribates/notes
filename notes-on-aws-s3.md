---
title: Notes on AWS S3
---

## Notes on AMAZON AWS S3


### How to know if a file exists in the bucket, and its size

This function does the trick:

```python
def file_in_cloud(client, bucket, key):
    response = client.list_objects_v2(Bucket=bucket, Prefix=key)
    for obj in response.get('Contents', []):
        if obj['Key'] == key:
            return True, obj['Size']
    return False, -1
```
