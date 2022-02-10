class StaticSiteScraper:
    '''
        Author: Retin P Kumar
        
        Methods
        =======
        
        url_parse
        ---------
        Returns the parsed html content of given url
        
        get_title
        ---------
        Returns the title of the given webpage
        
        get_all_links
        -------------
        Returns a list of all the links in the given url
        
        get_all_image_links
        -------------------
        Returns a list of all the links of images in the given url
        
        download_images
        ---------------
        Checks for an "images" directory within the current working directory.
        If not found, creates an "images" directory in the current working 
        directory. Saves all the images from the links returned by get_all_image_links
        method.       
    '''
    # importing libraries
    import os
    import datetime
    import requests
    from bs4 import BeautifulSoup as bs
    
    def __init__(self, url: str, parser: str='html.parser'):
        '''
            Parameters
            ----------
            url: url of webpage
            parser: object for parsing text files
            
            Returns
            -------
            self: object
        '''
        self.url = url
        self.parser = parser
    
    def url_parse(self): 
        '''
        A method for parsing the url
        
            Parameters
            ----------
            self: object
            
            Returns
            -------
            self.soup: parsed web html content
        '''
        try:
            # getting response from webpage
            data = self.requests.get(self.url).text
            # creating a html parsed object
            self.soup = self.bs(data, self.parser)
            return self.soup
        except Exception as e:
            print("Url not parsable. ", e)
        finally:
            # printing a prettified version of parsed html content
            print(self.soup.prettify())
    
    def get_title(self):
        '''
        A method for fetching the page title
        
            Parameters
            ----------
            self: object
            
            Returns
            -------
            title: webpage title text
        '''
        try:
            # fetching the webpage title
            title = self.soup.title.text
            print(title)
        except:
            print("Cannot find title.")
            
    def get_all_links(self):
        '''
        A method for fetching all links from the webpage
        
            Parameters
            ----------
            self: object
            
            Returns
            -------
            links: list of all links in the given url
        '''
        links=[] # list to store all the links
        try:
            # fetching all <a> tags
            self.a_tags = self.soup.find_all('a')
        except:
            print("Cannot find all <a> tags")
        
        # iterating through each element in the list of <a> tags
        for tag in self.a_tags:
            items = str(tag).split(" ")
            for item in items:
                if 'href' in item:
                    link_item = item.split("=")[1].split("\"")[1]
                    if 'http' in link_item or 'www' in link_item:
                        links.append(link_item)
        return links
            
    def get_all_image_links(self):
        '''
        A method for fetching all image links from the webpage
        
            Parameters
            ----------
            self: object
            
            Returns
            -------
            self.img_links: list of all image links in the given url
        '''
        self.img_links=[] # list to store all images
        
        # iterating through each element in the list of images
        img_tags = self.soup.find_all('img')
        for tag in img_tags:
            items = str(tag).split(" ")
            for item in items:
                if 'src' in item:
                    link_item = item.split("=")[1].split("\"")[1]
                    if 'http' in link_item or 'www' in link_item:
                        self.img_links.append(link_item)
        return self.img_links
        
    def download_images(self, image_list):
        '''
        A method for downloading images from the image links
        
            Parameters
            ----------
            self: object
            image_list: list of image links
            
            Returns
            -------
            Images in the image links inside an 'images' directory within current
            working directory.
        '''
        self.image_list = image_list
        try:
            # fetching today's date for directory name
            day = self.datetime.date.today().day
            month = self.datetime.date.today().month
            year = self.datetime.date.today().year

            date_ = str(day)+"-"+str(month)+"-"+str(year)+"_"
 
            # creating a new directory to store images
            if 'images' not in self.os.listdir():
                self.os.mkdir("images")
                self.os.chdir("images")
            
            self.os.mkdir(date_)
            self.os.chdir(date_)
            
            #image number
            img_no = 1
                
            # iterating through list of image links
            for link in self.image_list:
                # fetching image from webpage
                img_response = self.requests.get(link)
                
                #file format
                img_format = link.split(".")[-1]
                
                # creating a filename to store the image
                filename = "img" + str(img_no) + "." + img_format
                
                # saving the image using the filename
                with open(filename, "wb+") as f:
                    f.write(img_response.content)
                img_no += 1
                
            print(f"{len(self.img_links)} images downloaded succesfully into 'images/{date_}' directory.")    
        except Exception as e:
            print("Error while downloading images: ", e)