# Author:zylong
from scrapy.cmdline import execute
name = 'zhihu'
cmd = 'scrapy crawl {0}'.format(name)
execute(cmd.split())