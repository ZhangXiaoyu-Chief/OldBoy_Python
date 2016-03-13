webserber:
  hosts:
    - 123.59.44.38
    - 123.59.66.174
  actions:
      - cmd.run:
         command: 'df -h'
      - file.get:
         src: /etc/hosts
         dst: .
      - file.put:
         src: /home/zhangxiaoyu/PycharmProjects/OldBoy_Python/day9/shengxiao1.py
         dst: /home/ubuntu/