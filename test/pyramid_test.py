import numpy as np
import random
from functools import reduce
import urllib.request, urllib.error
import unittest
from tqdm import tqdm

class PyramidLibrary(unittest.TestCase):

    url = 'http://localhost:8081/isPyramid?word='

    def create_pyramid_word(self, length,upper=False,numbers=False):
        word = ''
        lower_choices = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        upper_choices = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        other_choices = ['0','1','2','3','4','5','6','7','8','9']
        if upper and numbers:
            selection = lower_choices+upper_choices+other_choices
            selection = list(np.random.choice(selection,min(length,len(selection)),replace=False))
        elif upper:
            selection = lower_choices+upper_choices
            selection = list(np.random.choice(selection,min(length,len(selection)),replace=False))
        elif numbers:
            selection = lower_choices+other_choices
            selection = list(np.random.choice(selection,min(length,len(selection)),replace=False))
        else:
            selection = lower_choices
            selection = list(np.random.choice(selection,min(length,len(selection)),replace=False))
        for i in range(min(length,len(selection))):
            word+=selection[i]*(i+1)
        return reduce(lambda x, y: x + y, random.sample(word,len(word))) 
    
    def get_status(self,u):
            try:
                resp = urllib.request.urlopen(u)
                #print(resp.read())
                return True
            except urllib.error.HTTPError as e:
                #print(e, e.code)
                return False
    
    def test_simple_pass(self):
        url = 'http://localhost:8081/isPyramid?word='
        word = 'banana'
        self.assertTrue(self.get_status(url+word))
    
    def test_simple_fail(self):
        url = 'http://localhost:8081/isPyramid?word='
        word = 'bandana'
        self.assertFalse(self.get_status(url+word))

    def test_lowercase(self):
        url = 'http://localhost:8081/isPyramid?word='
        for x in tqdm(range(1000)):
            for i in range(1,27):
                word = self.create_pyramid_word(i)
                self.assertTrue(self.get_status(url+word))
        
    def test_null(self):
        url = 'http://localhost:8081/isPyramid?word='
        self.assertFalse(self.get_status(url+'&num=True&caps=True'))
    
    def test_uppercase(self):
        url = 'http://localhost:8081/isPyramid?word='
        for x in tqdm(range(1000)):
            for i in range(1,53):
                word = self.create_pyramid_word(i,upper=True)
                self.assertTrue(self.get_status(url+word+'&caps=True'))
    
    def test_numbers(self):
        url = 'http://localhost:8081/isPyramid?word='
        for x in tqdm(range(1000)):
            for i in range(1,37):
                word = self.create_pyramid_word(i,numbers=True)
                self.assertTrue(self.get_status(url+word+'&num=True'))
    
    def test_all(self):
        url = 'http://localhost:8081/isPyramid?word='
        for x in tqdm(range(1000)):
            for i in range(1,63):
                word = self.create_pyramid_word(i,numbers=True,upper=True)
                self.assertTrue(self.get_status(url+word+'&num=True&caps=True'))
                


if __name__ == '__main__':
    unittest.main()

