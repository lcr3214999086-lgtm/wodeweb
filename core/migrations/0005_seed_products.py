from django.db import migrations


def seed(apps, schema_editor):
    Product = apps.get_model("core", "Product")
    Product.objects.using(schema_editor.connection.alias).create(**{'name': '全闪存储', 'category': '高性能存储', 'code': 'ALL-FLASH', 'description': '面向数据库、虚拟化与关键业务，规划低延迟、高并发的数据基础设施。', 'features': '关键业务数据\n虚拟化资源池\n数据库平台', 'sort_order': 0, 'is_published': True})
    Product.objects.using(schema_editor.connection.alias).create(**{'name': '混合存储', 'category': '通用存储', 'code': 'HYBRID STORAGE', 'description': '在性能、容量与成本之间取得平衡，为企业日常业务提供统一的数据承载。', 'features': '文件共享\n业务系统\n容量扩展', 'sort_order': 1, 'is_published': True})
    Product.objects.using(schema_editor.connection.alias).create(**{'name': '分布式存储', 'category': '规模化存储', 'code': 'SCALE-OUT', 'description': '面向持续增长的数据量，设计按需扩展的存储架构与统一管理方式。', 'features': '海量非结构化数据\n私有云\n数据归档', 'sort_order': 2, 'is_published': True})
    Product.objects.using(schema_editor.connection.alias).create(**{'name': '备份与容灾', 'category': '数据保护', 'code': 'DATA PROTECTION', 'description': '结合业务恢复目标，建立覆盖备份、恢复验证与异地保护的数据保障体系。', 'features': '备份管理\n恢复演练\n异地容灾', 'sort_order': 3, 'is_published': True})


class Migration(migrations.Migration):
    dependencies = [("core", "0004_product")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
