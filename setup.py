from setuptools import setup

setup(name='ansible_inventory_diff',
      version='0.1.0',
      packages=['ansible_inventory_diff'],
      entry_points={
          'console_scripts': [
              'ansible-inventory-diff = ansible_inventory_diff.__main__:main'
          ]
      },
      install_requires=['ansible>=2.4.0']
      )
