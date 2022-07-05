from import_export import resources
from import_export.fields import Field

# 使用：
# class objectModelResource(customResources):
#     class Meta:
#          model = objectModel

class customMetaOptions:
    model = None
    custom_extra_fields = {}
    custom_exclude_fields = []

class customMetaclass(type):
    '''获取meta的类'''
    def __new__(cls, name, bases, attrs):
        # 获取meta内容
        new_class = super().__new__(cls, name, bases, attrs)
        meta = customMetaOptions()
        options = getattr(new_class, 'Meta', None)
        for option in [option for option in dir(options)
                       if not option.startswith('_') and hasattr(options, option)]:
            setattr(meta, option, getattr(options, option))
        if getattr(meta, 'model') is None or meta.model is None:
            new_class._meta = meta
            return new_class
        # 创建对象
        fields = [i.name for i in meta.model._meta.fields if i.name not in meta.custom_exclude_fields]
        for key, value in meta.custom_extra_fields.items():
            fields.append(key)
        for field in fields:
            try:
                attrs[field] = Field(attribute='{}'.format(field), column_name=getattr(meta.model, field).field.verbose_name)
            except AttributeError:
                attrs[field] = Field(attribute='{}'.format(field), column_name=meta.custom_extra_fields[field])
        attrs['_meta'] = meta
        return super().__new__(cls, name, bases, attrs)

class customResourcesBase(metaclass=customMetaclass):
    pass

class customResourcesMix(type(customResourcesBase), type(resources.ModelResource)):
    pass

class customResources(resources.ModelResource, customResourcesBase, metaclass=customResourcesMix):
    pass