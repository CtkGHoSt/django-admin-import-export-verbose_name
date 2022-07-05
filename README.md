# django-admin-import-export-verbose_name
django admin替代django-import-export的resources.ModelResource类，让导入导出excel字段名为models的verbose_name

## 使用：
```
# ---------------- models.py ----------------

class objectModel(models.Model):
    field_a = models.CharField(verbose_name='字段A', max_length=16)
    field_b = models.CharField(verbose_name='字段B', max_length=16)
    field_unshow = models.CharField(verbose_name='不展示', max_length=16)
    
    class Meta:
        verbose_name = '测试表'

# ---------------- admin.py ---------------- 

from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

# from import_export import resources #<= 弃用，使用customResources代替
from yourApp.resources_base import customResources # 引入resources_base

from yourApp.models import objectModel


# class objectModelResource(resources.ModelResource):#<= 弃用，使用customResources代替
class objectModelResource(customResources):
    class Meta:
         model = objectModel
         custom_extra_fields = {'field_c': '字段C'}
         custom_exclude_fields = ['field_unshow', ]

@admin.register(objectModel)
class objectModelDetail(ImportExportActionModelAdmin):
    list_display = [i.name for i in objectModel._meta.fields if i.name != 'id']
    resource_class = objectModelResource

```
**输出：**  
|ID|字段A|字段B|字段C|   
|---|---|---|---|
|...|...|...|...| 
> 替代前：
> |ID|field_a|field_b|field_c|field_unshow|   
> |---|---|---|---|---|
> |...|...|...|...|...|

## TODO:    
* 自定义额外字段(custom_extra_fields)添加hook来输出
