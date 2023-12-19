from scipy.interpolate import interp1d
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os 
import pandas as pd
import re 



class ELEMENT:
    def __init__(self, symbol, name, Z, A, XrayMassCoefTable):
        self.symbol = symbol
        self.name = name
        self.Z = int(Z)
        self.A = float(A) # 元素平均原子量
        self.XrayMassCoefTable = XrayMassCoefTable
        self.Emin = 0.001
        self.Emax = 20
        
        # 根据precision对数据构建插值函数，插值函数的输入为能量，输出为μ/ρ和μen/ρ
        # 插值精度precision代表在Emin~Emax内插值的点数
        x = XrayMassCoefTable['Energy (MeV)']
        y1 = XrayMassCoefTable['μ/ρ (cm2/g)']
        y2 = XrayMassCoefTable['μen/ρ (cm2/g)']

        # 原始数据是对数坐标，因此需要在对数坐标下进行插值
        self.μ_ρ_log = interp1d(np.log10(x), np.log10(y1), kind='linear')
        self.μen_ρ_log = interp1d(np.log10(x), np.log10(y2), kind='linear')
    
    def μ_ρ(self, energy_lists):
        # 在使用这个函数时，希望传入是原始值，传出是原始值，故需要对μ_ρ_log进行包装
        return 10**self.μ_ρ_log(np.log10(energy_lists))
    
    def μen_ρ(self, energy_lists):
        return 10**self.μen_ρ_log(np.log10(energy_lists))

    def get_μ_ρ(self, energy_lists):
        # 返回能量为energy_lists的μ/ρ
        # 验证energy_lists的范围，只接受self.Emin~self.EmaxMeV的能量
        if not all(self.Emin <= energy <= self.Emax for energy in energy_lists):
            raise ValueError(f"Your input is {min(energy_lists)} ~ {max(energy_lists)} \n energy_lists must be in self.Emin~self.Emax MeV")
        return self.μ_ρ(energy_lists)
    
    def get_μen_ρ(self, energy_lists):
        # 返回能量为energy_lists的μen/ρ
        # 验证energy_lists的范围，只接受self.Emin~self.EmaxMeV的能量
        if not all(self.Emin <= energy <= self.Emax for energy in energy_lists):
            raise ValueError(f"Your input is {min(energy_lists)} ~ {max(energy_lists)} \n energy_lists must be in self.Emin~self.Emax MeV")
        return self.μen_ρ(energy_lists)
    
    def draw(self, precision = 100):
        # 绘制μ/ρ
        sns.set_style("whitegrid")
        # plt.style.use('seaborn-whitegrid')  # 设置科学绘图风格
        energy_lists = np.logspace(np.log10(self.Emin), np.log10(self.Emax), precision)
        energy_lists = np.clip(energy_lists, self.Emin, self.Emax)  # 限制能量范围在self.Emin~self.EmaxMeV
        # print(energy_lists)
        plt.loglog(energy_lists, self.get_μ_ρ(energy_lists),energy_lists, self.get_μen_ρ(energy_lists))  # 设置双对数坐标
        plt.xlim(self.Emin, self.Emax)
        plt.title(f"{self.Z}, {self.symbol}, {self.name},  μ/ρ and μen/ρ")
        plt.legend(['μ/ρ (cm2/g)', 'μen/ρ (cm2/g)'])
        plt.xlabel("Photon Energy (MeV)")
        plt.ylabel("μ/ρ and μen/ρ (cm2/g)")
        plt.grid(True, which="both", ls="--")  # 添加虚线网格
        plt.show()
        
    def __str__(self):
        return f"{self.symbol} {self.name} {self.Z}"
    
    def __repr__(self):
        return f"{self.symbol} {self.name} {self.Z}"
    
    def __eq__(self, other):
        return self.Z == other.Z
    
    def __lt__(self, other):
        return self.Z < other.Z
    
    def __gt__(self, other):
        return self.Z > other.Z
    
    def __le__(self, other):
        return self.Z <= other.Z
    
    def __ge__(self, other):
        return self.Z >= other.Z
    
    def __ne__(self, other):
        return self.Z != other.Z
    


class ELEMENTS:
    def __init__(self):
        self.elements = {}

    def add(self, element):
        self.elements[element.Z] = element

    def get(self, Z=None, symbol=None, name=None):
        if Z is not None:
            return self.elements[int(Z)]
        for element in self.elements.values():
            if symbol is not None and element.symbol == symbol:
                return element
            if name is not None and element.name == name:
                return element
        return None

    def print_all_elements(self):
        for element in self.elements.values():
            print(f"Symbol: {element.symbol}, Name: {element.name}, Z: {element.Z}")

    def get_ele_ratio(self, chemical):
        pattern = r'([A-Z][a-z]*)(\d*\.?\d*)'
        ele_ratio = []
        for element, ratio in re.findall(pattern, chemical):
            if not ratio:
                ratio = '1'
            ele_ratio.append((element, ratio))
        return ele_ratio

    def get_mass_ratio(self, ele_ratio):
        mole_mass = 0
        mass_ratio = []
        for ele, ratio in ele_ratio:
            mole_mass += self.get(symbol = ele).A * float(ratio)
        mass_ratio = [self.get(symbol = ele).A * float(ratio) / mole_mass for ele, ratio in ele_ratio]
        return mass_ratio

    def get_compound_u_p(self, chemical, energy_lists):
        ele_ratio = self.get_ele_ratio(chemical)
        mass_ratio = self.get_mass_ratio(ele_ratio)
        μ_ρ = 0
        element_ratio_u_p_list = []
        for i in range(len(ele_ratio)):
            element_ratio_u_p = self.get(symbol = ele_ratio[i][0]).get_μ_ρ(energy_lists) * mass_ratio[i]
            element_ratio_u_p_list.append(element_ratio_u_p)
            μ_ρ += element_ratio_u_p
        return μ_ρ, ele_ratio, element_ratio_u_p_list

    def calc_transmission(self, chemical, energy_lists, density, thickness):
        μ_ρ, aux1, aux2 = self.get_compound_u_p(chemical, energy_lists)
        return np.exp(-μ_ρ * density * thickness)*100 # 转换成百分比

    def draw_transmission(self, chemical, energy_lists, density, thickness, transmission_img_path=None, u_p_img_path=None):
        
        compound_μ_ρ, ele_ratio, element_ratio_u_p_list = self.get_compound_u_p(chemical, energy_lists)
        transmission = np.exp(-compound_μ_ρ * density * thickness)*100

        sns.set_style("whitegrid")  # Set the seaborn style to whitegrid
        
        # draw transmission
        plt.figure(figsize=(5, 3))  # 设置图形的大小为宽7英寸，高3英寸
        plt.plot(energy_lists, transmission) 
        plt.title(f"{chemical}, {density} g/cm3, {thickness} cm")
        plt.legend(['Transmission (%)'])
        plt.xlabel("Photon Energy (MeV)")
        plt.ylabel("Transmission (%)")
        plt.grid(True, which="both", ls="--")  # 添加虚线网格

        if transmission_img_path is None:
            plt.show()
        else:
            plt.tight_layout()  # 自动调整子图参数
            plt.savefig(transmission_img_path, dpi=150)
            plt.close()
        
        # draw μ/ρ
        plt.figure(figsize=(5, 3))  # 设置图形的大小为宽7英寸，高3英寸
        plt.loglog(energy_lists, compound_μ_ρ)
        for i in range(len(element_ratio_u_p_list)):
            plt.loglog(energy_lists, element_ratio_u_p_list[i], '--')
        plt.legend(['μ/ρ (cm2/g)'] + [f"{ele_ratio[i][0]} {ele_ratio[i][1]}" for i in range(len(ele_ratio))])
        plt.xlabel("Photon Energy (MeV)")
        plt.ylabel("μ/ρ (cm2/g)")
        plt.grid(True, which="both", ls="--")
        plt.title(f"Contributions of different elements to μ_ρ")
        if u_p_img_path is None:
            plt.show()
        else:
            plt.tight_layout()  # 自动调整子图参数
            plt.savefig(u_p_img_path, dpi=150)
            plt.close()

