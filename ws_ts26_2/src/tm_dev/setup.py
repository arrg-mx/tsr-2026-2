from setuptools import find_packages, setup

package_name = 'tm_dev'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arrgusr',
    maintainer_email='erik.pena@ingenieria.unam.edu',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'simple_node_py = tm_dev.pubsher_node:main',
            'publisher_node_py = tm_dev.publisher_node:main',
            'subscriber_node_py = tm_dev.subscriber_node:main'
        ],
    },
)
