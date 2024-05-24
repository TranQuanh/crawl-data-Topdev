import scrapy
import json
from topdev.items import JobItem
class TopdevspiderSpider(scrapy.Spider):
    name = "topdevspider"
    allowed_domains = ["topdev.vn"]
  
  
    def start_requests(self):
            url ="https://api.topdev.vn/td/v2/jobs?fields[job]=id,slug,title,salary,company,extra_skills,skills_str,skills_arr,skills_ids,job_types_str,job_levels_str,job_levels_arr,job_levels_ids,addresses,status_display,detail_url,job_url,salary,published,refreshed,applied,candidate,requirements_arr,packages,benefits,content,features,is_free,is_basic,is_basic_plus,is_distinction&fields[company]=slug,tagline,addresses,skills_arr,industries_arr,industries_str,image_cover,image_galleries,benefits&page=2&locale=vi_VN&ordering=jobs_new"
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
            yield scrapy.Request(url,callback=self.parse,headers=headers)
            
            
    def parse(self, response):
        raw_data = response.body
        data= json.loads(raw_data)
        jobs = data['data']
        for job in jobs:
            title = job['title']
            full_address = job['addresses']['full_addresses'][0]
            
            company = job['company']
            company_name = company['display_name']
            company_detail_url = company['detail_url']
            company_image_logo = company['image_logo']
            company_industries = company['industries_str']
            
            detail_url = job['detail_url']
            job_level = job['job_levels_str']
            skills = job['skills_str']
            job_type = job['job_types_str']
            
            salary = job['salary']
            salary_job = ""
            is_negotible = salary['is_negotiable']
            max = salary['max']
            min = salary['min']
            currency = salary['currency']
            if is_negotible ==1:
                salary_job = "Thuong Luong"
            else:
                salary_job = f"Tu {min} {currency} den {max} {currency}"
                
            published_date = job['published']['date']
            refreshed_date = job['refreshed']['date']
            # job_item = JobItem()
            
            # job_item['title'] = title
            # job_item['full_address'] =  full_address
            # job_item['company_name'] = company_name
            # job_item['detail_url'] = detail_url
            # job_item['job_level'] = job_level
            # job_item['skills'] = skills
            # job_item['job_type'] = job_type
            # job_item['salary'] = salary
            
            # yield job_item
            yield{
                'title':title,
                  'full_address' : full_address,
                  'company_name' : company_name, 
                  'company_detail_url':company_detail_url,
                  'company_image_logo': company_image_logo, 
                  'company_industries': company_industries, 
                  'detail_url' : detail_url,
                  'job_level' :job_level,
                  'skills' :skills,
                  'job_type' : job_type,
                  'salary' : salary_job,
                  'published': published_date,
                  'refreshed':refreshed_date,
                  }
                  
            
            
            
        meta = data['meta']
        current_page = meta['current_page']
        last_page = meta['last_page']
        if current_page <= last_page:
            next_page_url = "https://api.topdev.vn/td/v2/jobs?fields[job]=id,slug,title,salary,company,extra_skills,skills_str,skills_arr,skills_ids,job_types_str,job_levels_str,job_levels_arr,job_levels_ids,addresses,status_display,detail_url,job_url,salary,published,refreshed,applied,candidate,requirements_arr,packages,benefits,content,features,is_free,is_basic,is_basic_plus,is_distinction&fields[company]=slug,tagline,addresses,skills_arr,industries_arr,industries_str,image_cover,image_galleries,benefits&page="+ str(current_page+1)+"&locale=vi_VN&ordering=jobs_new"
            yield response.follow(next_page_url,callback=self.parse)
     
     
     
     
     
     
            
    # def parse_job_page(self,response):
    #     # job header 
    #     detail_job_header = response.css('section.sticky.top-0 div.flex-initial.flex-col ')
    #     job_name = detail_job_header.css('h1::text').get()
    #     job_company = detail_job_header.css('p.my-1::text').get()
    #     job_address = detail_job_header.css('div.text-base div.mb-2.flex  div::text').get()
        
    #     comments = response.css('div.rounded div.prose.mb-4  ul li ')
    #     all_comment =""
    #     for coment in comments:
    #             all_comment += coment.css('span::text').get()
    #             all_comment +=". "
    #     trach_nhiem_cong_viec = response.css('div.rounded div.mb-4.border-b')[1]
    #     trach_nhiem =  trach_nhiem_cong_viec.css('div.prose ul li')
    #     responsibility = ""
    #     for comment in trach_nhiem:
    #          responsibility += comment.css('span::text').get()
    #          responsibility +=". "
        
    #     yield{
    #          "job_name" : job_name,
    #          "job_company" : job_company,
    #          "job_adress" : job_address,
    #          "all_comment" : all_comment,
    #          "responsibility" : responsibility 
    #     }
        
             
