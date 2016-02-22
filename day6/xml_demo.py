#!/usr/bin/env python
# coding:utf-8
'''
Created on: 

@author: 张晓宇

Email: 61411916@qq.com

Version: 1.0

Description:

Help:
'''
if __name__ == '__main__':
    import xml.etree.ElementTree as ET
    tree = ET.parse('test.xml') # 读取xml文件，并以Element对象的形式保存

    root = tree.getroot() # 获取根
    # for child in root: # 遍历root下的子标签
    #     print(child.tag, child.attrib) # 打印标签名和属性
    #     for i in child:
    #         print(i.tag, i.text, i.attrib) # 打印标签名值和属性
    # for node in root.iter('year'): # 仅遍历标签名为year的标签
    #     print(node.tag, node.text, node.attrib)
    # 修改，比如我们把year标签的值都加1
    # for node in root.iter('year'): # 遍历year标签
    #     node.text = str(int(node.text) + 1) # 将year标签的值+1，注意，读出来的标签的值都是字符串形式，注意数据类型转换
    #     node.set('updated', 'yes') # 更新该标签
    # tree.write('test_2.xml') # 将结果写到文件，可以写到源文件也可以写到新的文件中

    # for country in root.findall('country'): # 遍历所有country标签
    #    rank = int(country.find('rank').text) # 在country标签查找名为rank的纸标签
    #    if rank > 50: # 判断如果rank标签的值大于50
    #        root.remove(country) # 删除该标签
    #
    # tree.write('test_3.xml')
# import xml.etree.ElementTree as ET
# tree = ET.parse('test.xml') # 读取xml文件，并以Element对象的形式保存
#
# root = tree.getroot() # 获取根
# for country in root.findall('country'): # 遍历所有country标签
#    rank = int(country.find('rank').text) # 在country标签查找名为rank的纸标签
#    if rank > 50: # 判断如果rank标签的值大于50
#        root.remove(country) # 删除该标签
#
# tree.write('test_3.xml')
#     r = root.iter('country')
#     r.find('rank')
import xml.etree.ElementTree as ET


new_xml = ET.Element("namelist") # 新建根节点，或者说xml对象
name = ET.SubElement(new_xml,"name",attrib={"enrolled":"yes"}) # 给新xml对象创建子标签
age = ET.SubElement(name,"age",attrib={"checked":"no"}) # name标签在创建子标签age，attrib变量为属性
sex = ET.SubElement(name,"sex")
sex.text = '33' # 给标签赋值
name2 = ET.SubElement(new_xml,"name",attrib={"enrolled":"no"})
age = ET.SubElement(name2,"age")
age.text = '19'


et = ET.ElementTree(new_xml) #生成文档对象
et.write("test.xml", encoding="utf-8",xml_declaration=True) # 将xml对象保存到文件xml_declaration表示xml文档的声明

ET.dump(new_xml) #打印生成的格式