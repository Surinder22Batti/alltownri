# -*- coding: utf-8 -*-
import scrapy
from alltownri.items import AlltownriItem
from collections import OrderedDict


class AlltownSpider(scrapy.Spider):
    name = 'alltown'
    allowed_domains = ['alltownri.com']
    # start_urls = ['http://alltownri.com/']
    start_urls = ["https://www.alltownri.com/search/results/?state=RI&county=all&city=all&beds_min=all&baths_min=all&list_price_min=175000&list_price_max=325000&type=res"]

    def parse(self, response):
        print("url ::::::::::::: ",response.url)
        items = response.xpath("//div[@class='property-detail-section']/div/div/a/@href").extract()
        print("Total : ",len(items))
        if items:
            for item in items:
                link = "https://www.alltownri.com{0}".format(item)
                # yield scrapy.Request(url=link, callback=self.parse_property)
                # break

        next_page_list = response.xpath("//ul[@class='pagination']/li")[-2].xpath("./a/text()").extract_first()
        if next_page_list:
            pages = int(next_page_list)
            for page in range(2, pages):
                next_url = "https://www.alltownri.com/search/results/?state=RI&county=all&city=all&beds_min=all&baths_min=all&list_price_min=175000&list_price_max=325000&type=res&page={0}".format(page)
                yield scrapy.Request(url=next_url, callback=self.parse_page_items)
                break
    
    def parse_page_items(self, response):
        items = response.xpath("//div[@class='property-detail-section']/div/div/a/@href").extract()
        print("Total : ",len(items))
        if items:
            for item in items:
                link = "https://www.alltownri.com{0}".format(item)
                yield scrapy.Request(url=link, callback=self.parse_property)

    def parse_property(self, response):
        # print("---------------------------------------")
        print("YYYYYYYYYYYYYYYYYYYYYYY")
        print(response.url)
        url = response.url
        image = response.xpath("//meta[@property='og:image']/@content").extract_first()
        # home_id = response.url.split("RIS-")[-1].split("/")[0].strip()
        address_txt = response.xpath("//div[@class='small-12 columns prop-address']/h1/text()").extract_first()
        name = ""
        address = ""
        city = ""
        postal_code = ""
        region = ""
        availability = "for_sale"
        listing_type = "for_sale_by_agent"
        if address_txt:
            address_txt = address_txt.split(", ")
            try:
                name = address_txt[0].strip() + ", " + address_txt[1].strip()
            except:
                pass
            try:
                address = address_txt[0].strip()
            except:
                pass
            try:
                city = address[1].strip()
            except:
                pass
            try:
                postal_code = address_txt[-1].strip().split()[-1].strip()
                region_txt = address_txt[-1].strip().split()[0].strip()
                if region_txt == "RI":
                    region = "Rhode Island"
                else:
                    region = region_txt
            except:
                pass

        country = "United States"
            
        # print("Name : ",name)
        # print("Address : ",address)
        # print("City : ",city)
        # print("Region : ",region)
        # print("country : ",country)
        # print("postal_code : ",postal_code)

        price = response.xpath(".//dt[contains(text(), 'List Price')]/following-sibling::dd/text()").extract_first()
        mls_number = response.xpath(".//dt[contains(text(), 'MLS#')]/following-sibling::dd/text()").extract_first()
        status = response.xpath(".//dt[contains(text(), 'Status')]/following-sibling::dd/text()").extract_first()
        type1 = response.xpath(".//dt[contains(text(), 'Type')]/following-sibling::dd/text()").extract_first()
        city = response.xpath(".//dt[contains(text(), 'City')]/following-sibling::dd/text()").extract_first()
        county = response.xpath(".//dt[contains(text(), 'County')]/following-sibling::dd/text()").extract_first()
        bedrooms = response.xpath(".//dt[contains(text(), 'Bedrooms')]/following-sibling::dd/text()").extract_first()
        bathrooms = response.xpath(".//dt[contains(text(), 'Bathrooms')]/following-sibling::dd/text()").extract_first()
        size = response.xpath(".//dt[contains(text(), 'Living Area')]/following-sibling::dd/text()").extract_first()
        year = response.xpath(".//dt[contains(text(), 'Year')]/following-sibling::dd/text()").extract_first()
        # description = response.xpath("//div[@class='additional-information-element']/p/text()").extract_first()
        unit = "sqft"
        try:
            unit_txt = response.xpath("//dd[@class='price']/ancestor::dl/dt")[-2].xpath("./text()").extract_first()
            if unit_txt:
                unit = unit.lower()
        except:
            pass
        description = ""
        if bedrooms and bathrooms and size and unit:
            description = bedrooms + "BR | " + bathrooms + "BA | " + size + " " + unit

        if mls_number:
            mls_number = mls_number.replace("RIS-", "").strip()
        item = OrderedDict()
        item['home_listing_id'] = mls_number
        item['name'] = name
        item['availability'] = availability
        item['address.addr1'] = address
        item['address.city'] = city
        item['address.region'] = region
        item['address.country'] = country
        item['address.postal_code'] = postal_code
        item['image[0].url'] = image
        item['price'] = price
        item['url'] = url
        item['description'] = description
        item['num_beds'] = bedrooms
        item['num_baths'] = bathrooms
        item['property_type'] = type1
        item['listing_type'] = listing_type
        item['year_built'] = year
        item['size'] = size
        item['status'] = status
        item['mls_num'] = mls_number
        item['county'] = county
        print("#"*100)
        yield item

















# # -*- coding: utf-8 -*-
# import scrapy
# from alltownri.items import AlltownriItem
# from collections import OrderedDict


# class AlltownSpider(scrapy.Spider):
#     name = 'alltown'
#     allowed_domains = ['alltownri.com']
#     # start_urls = ['http://alltownri.com/']
#     start_urls = ["https://www.alltownri.com/search/results/?state=RI&county=all&city=all&beds_min=all&baths_min=all&list_price_min=175000&list_price_max=325000&type=res"]

#     def parse(self, response):
#         results = response.xpath("//div[@class='property-detail-section']/div/div/a/@href").extract()
#         total = len(results)
#         print("Total : ",total)
#         if results:
#             for result in results:
#                 result = "https://www.alltownri.com{0}".format(result)
#                 yield scrapy.Request(url=result, callback=self.parse_property)
#                 # break

#         # next_page_list = response.xpath(self.next_xpath).extract()
#         # if next_page_list:
#         #     next_page = next_page_list[-1]
#         #     print("Scraping next page", next_page)
#         #     if next_page:
#         #         next_page = response.urljoin(next_page)
#         #         yield scrapy.Request(next_page, callback=self.parse)
        

#     def parse_property(self, response):
#         # print("---------------------------------------")
#         # item = AlltownriItem()
#         url = response.url
#         image = response.xpath("//meta[@property='og:image']/@content").extract_first()
#         home_id = response.url.split("RIS-")[-1].split("/")[0].strip()
#         address_txt = response.xpath("//div[@class='small-12 columns prop-address']/h1/text()").extract_first()
#         availability = "for_sale"
#         listing_type = "for_sale_by_agent"
#         if address_txt:
#             address_txt = address_txt.split(", ")
#             try:
#                 name = address_txt[0].strip() + ", " + address_txt[1].strip()
#             except:
#                 name = ""
#             try:
#                 address = address_txt[0].strip()
#             except:
#                 address = ""
#             try:
#                 city = address[1].strip()
#             except:
#                 city = ""
#             try:
#                 postal_code = address_txt[-1].strip().split()[-1].strip()
#                 region_txt = address_txt[-1].strip().split()[0].strip()
#                 if region_txt == "RI":
#                     region = "Rhode Island"
#                 else:
#                     region = region_txt
#             except:
#                 postal_code = ""
#                 region = ""

#         country = "United States"
            
#         # print("Name : ",name)
#         # print("Address : ",address)
#         # print("City : ",city)
#         # print("Region : ",region)
#         # print("country : ",country)
#         # print("postal_code : ",postal_code)

#         price = response.xpath(".//dt[contains(text(), 'List Price')]/following-sibling::dd/text()").extract_first()
#         mls_number = response.xpath(".//dt[contains(text(), 'MLS#')]/following-sibling::dd/text()").extract_first()
#         status = response.xpath(".//dt[contains(text(), 'Status')]/following-sibling::dd/text()").extract_first()
#         type1 = response.xpath(".//dt[contains(text(), 'Type')]/following-sibling::dd/text()").extract_first()
#         city = response.xpath(".//dt[contains(text(), 'City')]/following-sibling::dd/text()").extract_first()
#         county = response.xpath(".//dt[contains(text(), 'County')]/following-sibling::dd/text()").extract_first()
#         bedrooms = response.xpath(".//dt[contains(text(), 'Bedrooms')]/following-sibling::dd/text()").extract_first()
#         bathrooms = response.xpath(".//dt[contains(text(), 'Bathrooms')]/following-sibling::dd/text()").extract_first()
#         size = response.xpath(".//dt[contains(text(), 'Living Area')]/following-sibling::dd/text()").extract_first()
#         year = response.xpath(".//dt[contains(text(), 'Year')]/following-sibling::dd/text()").extract_first()
#         # description = response.xpath("//div[@class='additional-information-element']/p/text()").extract_first()
#         unit = response.xpath("//dd[@class='price']/ancestor::dl/dt")[-2].xpath("./text()").extract_first()
#         if unit:
#             unit = unit.lower()
#         description = ""
#         if bedrooms and bathrooms and size and unit:
#             description = bedrooms + "BR | " + bathrooms + "BA | " + size + " " + unit

#         if mls_number:
#             mls_number = mls_number.replace("RIS-", "").strip()
#         item = OrderedDict()
#         item['home_listing_id'] = home_id
#         item['name'] = name
#         item['availability'] = availability
#         item['address.addr1'] = address
#         item['address.city'] = city
#         item['address.region'] = region
#         item['address.country'] = country
#         item['address.postal_code'] = postal_code
#         item['image[0].url'] = image
#         item['price'] = price
#         item['url'] = url
#         item['description'] = description
#         item['num_beds'] = bedrooms
#         item['num_baths'] = bathrooms
#         item['property_type'] = type1
#         item['listing_type'] = listing_type
#         item['year_built'] = year
#         item['size'] = size
#         item['status'] = status
#         item['mls_num'] = mls_number
#         item['county'] = county
#         print("#"*100)
#         yield item
