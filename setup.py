import os
from setuptools import setup

version = '1.0.0'

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()
    setup(
        name='designmate',
        version=version,
        url='https://github.com/gabriellopesdesouza2002/DesignMate',
        license='MIT License',
        author='Gabriel Lopes de Souza',
        long_description=readme,
        long_description_content_type="text/markdown",
        author_email='https://www.linkedin.com/in/gabriel-lopes2002',
        keywords=[
            'selenium', 
            'automation', 
            'web-automation', 
            'robots', 
            'flask', 
            'web-development', 
            'python', 
            'automation-tools', 
            'web-scraping', 
            'testing', 
            'browser-automation', 
            'selenium-webdriver', 
            'selenium-framework', 
            'python-automation', 
            'web-robots', 
            'automation-scripts', 
            'selenium-utils', 
            'flask-templates', 
            'flask-automation', 
            'python-tools'
        ],
        description=u'DesignMate é uma biblioteca Python que facilita o desenvolvimento de robôs de automação web com Selenium e a criação de projetos Flask seguindo padrões de projeto. Com funções utilitárias e templates prontos, o DesignMate ajuda desenvolvedores a acelerar a criação de automações robustas e APIs Flask bem estruturadas. Ideal para quem busca produtividade e boas práticas em automação e desenvolvimento web.',        
        packages= [
            os.path.join('designmate', 'flask'),
            os.path.join('designmate', 'utils'),
        ],
        install_requires= [],
)
