from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import BarChartModule
from mesa.datacollection import DataCollector
from math import ceil
from numpy import var, mean
import random



NUMBER_OF_PEOPLE = 6  # 人数
SEND_RED_PACKET_AMOUNT = 100  # 发红包金额


def CDF(a, A, u) -> float:
    """
    计算给定均匀随机数u的CDF逆函数值。

    :param A: 参数A
    :param a: 参数a
    :param u: 均匀分布随机数，范围在[0,1]
    :return: 对应的CDF逆函数值
    """
    if a <= A:
        return ceil(a*100)/100
    n = (a - 2 * A) / (a - A)
    k = (1 - n) * a**(n - 1)
    if (1 - n)/k <= 0:
        return 0
    return ceil((u * (1 - n) / k)**(1 / (1 - n))*100)/100


class Person(Agent):
    """可以抢红包更新个人财富的的人"""

    def __init__(self, unique_id, model, w) -> None:
        super().__init__(unique_id, model)
        self.wealth: float = w
        self.grab_record: list = [0]

    def wealth_report(self) -> float:
        return self.wealth
    
    def grab_amount_variance_report(self) -> float:
        return var(self.grab_record)
    
    def grab_amount_mean_report(self) -> float:
        return mean(self.grab_record)

    def grab_red_packet(self, red_packet_amount) -> None:
        if self.unique_id == self.model.N - 1:
            # 最后一个人抢到最后一张红包
            grab_amount = red_packet_amount
            print(f"agent{self.unique_id}抢到最后一张红包：{grab_amount:.2f}")
        else:
            # 计算抢到的红包金额
            grab_amount = CDF(red_packet_amount, SEND_RED_PACKET_AMOUNT / NUMBER_OF_PEOPLE, random.uniform(0, 1))
            if grab_amount >= red_packet_amount:
                print(f"agent{self.unique_id}抢到最后一张红包：{
                      red_packet_amount:.2f}")
            else:
                print(f"agent{self.unique_id}抢到红包：{grab_amount:.2f}")

        # 更新个人财富
        self.wealth += grab_amount
        return grab_amount

    def step(self) -> None:
        # 只有当红包金额大于0时才尝试抢红包
        if self.model.send_red_packet_amount[0] > 0:
            grab_amount = self.grab_red_packet(
                self.model.send_red_packet_amount[0])
            # 更新模型中的红包金额
            self.grab_record.append(grab_amount)
            self.model.send_red_packet_amount[0] -= grab_amount


# 创建一个图表模块，用于显示每个财富级别的代理数量
chart_element = ChartModule([{"Label": f"AW{i}", "Color": f"hsla({i*360/NUMBER_OF_PEOPLE}, 100%, 50%, 0.5"} for i in range(NUMBER_OF_PEOPLE)],
                            data_collector_name="datacollector")

bar_chart_element1 = BarChartModule([{"Label": f"AM{i}", "Color": f"hsl({i*360/NUMBER_OF_PEOPLE}, 100%, 50%"} for i in range(NUMBER_OF_PEOPLE)],
                                    data_collector_name="datacollector")

bar_chart_element2 = BarChartModule([{"Label": f"AV{i}", "Color": f"hsl({i*360/NUMBER_OF_PEOPLE}, 100%, 50%"} for i in range(NUMBER_OF_PEOPLE)],
                            data_collector_name="datacollector")


class RedPacketModel(Model):
    """红包游戏模型"""

    def __init__(self, N, A) -> None:
        self.N = N
        self.send_red_packet_amount = [A]

        self.schedule = SimultaneousActivation(self)

        # 随机生成N个收发红包的人
        for i in range(N):
            p = Person(i, self, w=0)
            self.schedule.add(p)
        
        wealth_dict = {f"AW{agent.unique_id}": agent.wealth_report for agent in self.schedule.agents}
        variance_dict = {f"AV{agent.unique_id}": agent.grab_amount_variance_report for agent in self.schedule.agents}
        mean_dict = {f"AM{agent.unique_id}": agent.grab_amount_mean_report for agent in self.schedule.agents}
        # 合并两个字典
        combined_dict = {**wealth_dict, **variance_dict, **mean_dict}
        self.datacollector = DataCollector(
            model_reporters=combined_dict
        )

    def step(self) -> None:
        # 随机发放红包
        self.schedule.step()
        self.send_red_packet_amount[0] = SEND_RED_PACKET_AMOUNT
        self.datacollector.collect(self)


# if __name__ == "__main__":
#     model = RedPacketModel(N=NUMBER_OF_PEOPLE, A=SEND_RED_PACKET_AMOUNT)
#     for i in range(10):
#         print(f"第{i+1}轮：")
#         model.step()
#         for agent in model.schedule.agents:
#             # 保留两位小数
#             print(f"agent{agent.unique_id}的当前金额：{agent.wealth:.2f}")
if __name__ == "__main__":
    # 创建ModularServer实例
    server = ModularServer(RedPacketModel,
                           [chart_element,bar_chart_element1,bar_chart_element2],
                           "Red Packet Model",
                           {"N": NUMBER_OF_PEOPLE, "A": SEND_RED_PACKET_AMOUNT})

    # 启动服务器
    server.port = 8523  # The default
    server.launch()