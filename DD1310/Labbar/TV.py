class TV:
    def __init__(self, tv_name, max_channel, current_channel, max_volume,current_volume):
        self.tv_name=tv_name
        self.current_volume= current_volume
        self.current_channel=current_channel
        self.max_volume=max_volume
        self.max_channel = max_channel

    def change_channel(self,new_channel):

        if new_channel<=self.max_channel and new_channel>=0:
            self.current_channel = new_channel
            return True
        else:
            return False
        
    def increase_volume(self):
        if self.current_volume<=self.max_volume:
            self.current_volume+=1
            return True
        else:
            return False
    def decrease_volume(self):
        if self.current_volume>=0 and self.current_volume<=self.max_volume:
            self.current_volume-=1
            return True
        else:
            return False
    def __str__(self):
        return "{},channel:{},volume:{}".format(
            self.tv_name,self.current_channel,self.current_volume)

    def str_for_file(self):
        return "{}, Max channel:{}, Current Channel:{}, Max volume:{}, Current volume:{}".format(
            self.tv_name ,self.max_channel,self.current_channel, self.max_volume, self.current_volume)
    
tv=TV("Vardagsrums TV",100,22,10,9)
tv2=TV("Sovrums TV",50,7,20,4)
print(tv)
print(tv2)
print(tv.increase_volume())
print(tv)
print(tv2)
print(tv2.change_channel(55))
print(tv)




