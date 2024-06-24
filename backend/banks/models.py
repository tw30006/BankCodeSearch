from django.db import models
import re

class Bank(models.Model):
    headOfficeCode = models.CharField(max_length=10, default="")
    branchOfficeCode = models.CharField(max_length=10, blank=True, null=True, default="")
    headOffice = models.CharField(max_length=100,default="")
    branchOffice = models.CharField(max_length=100,default="")
    name = models.CharField(max_length=100,default="")
    address = models.CharField(max_length=250,default="")
    tel = models.CharField(max_length=20,default="")
    
    def save(self, *args, **kwargs):
        match = re.search(r'(.*?)(銀行|信用合作社|證券|公司|商銀)(股份有限公司)?(.*)', self.name)
        if match:
            self.headOffice = match.group(1) + match.group(2)
            self.branchOffice = re.sub(r'股份有限公司|有限公司|集團', '', match.group(4)).strip()
        else:
            self.headOffice = self.name
            self.branchOffice = ''

        self.address = self.address if self.address else 'null'
        self.tel = self.tel if self.tel else ''

        super().save(*args, **kwargs)