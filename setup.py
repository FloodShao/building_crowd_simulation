from setuptools import setup

package_name = 'building_crowd_simulation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[
        'building_navmesh',
        'parsing_map',
        'navmesh_generator',
        'configfile_generator'
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'shapely', 'pyyaml'],
    zip_safe=True,
    maintainer='fred',
    maintainer_email='fred.guoliang.shao@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'building_navmesh = '
            'building_navmesh.test:main',
            'navmesh_generator = '
            'navmesh_generator.navmesh_generator:main',
            'configfile_generator = '
            'configfile_generator.configfile_generator:main',
        ],
    },
)
