from django.db import models


class Product(models.Model):
    name = models.CharField('产品名称', max_length=120)
    category = models.CharField('产品分类', max_length=60)
    code = models.CharField('产品标识', max_length=80, blank=True)
    description = models.TextField('产品简介')
    features = models.TextField('产品特点', blank=True, help_text='每行填写一项特点。')
    selection_notes = models.TextField('选型说明', blank=True)
    image = models.ImageField('产品图片', upload_to='products/%Y/%m/', blank=True)
    sort_order = models.PositiveIntegerField('排序', default=0, help_text='数字越小越靠前。')
    is_published = models.BooleanField('已上架', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '产品管理'
        verbose_name_plural = '产品管理'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    contact = models.CharField('联系人', max_length=60)
    phone = models.CharField('联系电话', max_length=30)
    company = models.CharField('公司/品牌', max_length=120)
    request_type = models.CharField('需求类型', max_length=40)
    quantity = models.PositiveIntegerField('预计数量')
    city = models.CharField('交付城市', max_length=80)
    budget = models.CharField('预算区间', max_length=40)
    description = models.TextField('需求说明', max_length=3000)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)

    class Meta:
        db_table = 'contract'
        verbose_name = '联系表单'
        verbose_name_plural = '联系表单'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.company} - {self.contact}'
