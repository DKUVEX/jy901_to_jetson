# coding:UTF-8
from abc import abstractmethod, ABCMeta

"""
操作设备接口类
"""


class IOperatingEquipment(metaclass=ABCMeta):

    @abstractmethod
    def SetPortName(self, portName):
        """
        设置串口号
        :param self:
        :param portName:
        :return:
        """
        pass

    def SetBaudrate(self, baudrate):
        """
        设置波特率
        :param self:
        :param baudrate:
        :return:
        """
        pass

    def Open(self):
        """
        打开串口
        :param self:
        :return:
        """
        pass

    def IsOpen(self):
        """
        串口是否打开
        :return:
        """
        pass

    def  UnlockReg(self):
        """
        解锁
        :return:
        """
        pass

    def AppliedCalibration(self):
        """
        加计校准
        :return:
        """
        pass

    def BeginFiledCalibration(self):
        """
        开始磁场校准
        :return:
        """
        pass

    def EndFiledCalibration(self):
        """
        结束磁场校准
        :return:
        """
        pass

    def Close(self):
        """
        关闭串口
        :param self:
        :return:
        """
        pass