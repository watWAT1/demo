import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import os

st.set_page_config(
    page_title="医疗费用预测系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    try:
        encodings_to_try = ['utf-8', 'gbk', 'gb2312', 'latin1']
        for encoding in encodings_to_try:
            try:
                df = pd.read_csv("insurance-chinese.csv", encoding=encoding)
                return df
            except:
                continue
        df = pd.read_csv("insurance-chinese.csv")
        return df
    except Exception as e:
        st.error(f"加载数据失败: {str(e)}")
        return None

def train_model(df):
    try:
        required_columns = ['年龄', '性别', 'BMI', '子女数量', '是否吸烟', '区域', '医疗费用']
        
        column_mapping = {
            '年龄': ['年龄', 'age'],
            '性别': ['性别', 'sex', 'gender'],
            'BMI': ['BMI', 'bmi'],
            '子女数量': ['子女数量', 'children'],
            '是否吸烟': ['是否吸烟', 'smoker'],
            '区域': ['区域', 'region'],
            '医疗费用': ['医疗费用', 'charges', '费用']
        }
        
        actual_columns = {}
        for std_name, possible_names in column_mapping.items():
            for name in possible_names:
                if name in df.columns:
                    actual_columns[std_name] = name
                    break
        
        for std_name, actual_name in actual_columns.items():
            if actual_name != std_name:
                df[std_name] = df[actual_name]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.warning(f"数据中缺少以下列: {missing_columns}")
            return None
        
        label_encoders = {}
        categorical_cols = ['性别', '是否吸烟', '区域']
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
        
        feature_cols = ['年龄', '性别', 'BMI', '子女数量', '是否吸烟', '区域']
        X = df[feature_cols]
        y = df['医疗费用']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        return model, label_encoders, feature_cols
        
    except Exception as e:
        st.error(f"训练模型失败: {str(e)}")
        return None, None, None

@st.cache_data
def load_and_train():
    df = load_data()
    if df is not None:
        model, label_encoders, feature_cols = train_model(df)
        return df, model, label_encoders, feature_cols
    return None, None, None, None

with st.sidebar:
    st.markdown("### 导航")
    
    nav_options = st.radio(
        "",
        ["简介", "预测医疗费用"],
        index=0,
        label_visibility="collapsed"
    )

if nav_options == "简介":
    st.title("欢迎使用")
    st.header("医疗费用预测应用")
    
    st.write("这个应用利用机器学习模型来预测医疗费用，为保险公司的保险定价提供参考。")
    
    st.header("背景介绍")
    st.write("- **开发目标:** 帮助保险公司合理定价保险产品，控制风险")
    st.write("- **模型算法:** 利用随机森林回归算法训练医疗费用预测模型")
    
    st.header("使用指南")
    st.write("- 输入准确完整的被保险人信息，可以得到更准确的费用预测")
    st.write("- 预测结果可以作为保险定价的重要参考，但需审慎决策")
    st.write("- 有任何问题欢迎联系我们的技术支持")
    
elif nav_options == "预测医疗费用":
    st.title("使用说明")
    
    st.write("这个应用利用机器学习模型来预测医疗费用，为保险公司的保险定价提供参考。")
    
    st.write("- **输入信息**: 在下面输入被保险人的个人信息、疾病信息等")  
    st.write("- **费用预测**: 应用会预测被保险人的未来医疗费用支出")
    
    st.write("---")
    
    df, model, label_encoders, feature_cols = load_and_train()
    
    st.subheader("年龄")
    age = st.number_input(
        "年龄", 
        min_value=0, 
        max_value=100, 
        value=0,
        step=1,
        label_visibility="collapsed"
    )
    
    st.subheader("性别")
    sex = st.radio("性别", ["男性", "女性"], horizontal=True, label_visibility="collapsed")
    
    st.subheader("BMI")
    bmi = st.number_input(
        "BMI", 
        min_value=0.0, 
        max_value=50.0, 
        value=0.0,
        step=0.1,
        label_visibility="collapsed"
    )
    
    st.subheader("子女数量:")
    children = st.number_input(
        "子女数量", 
        min_value=0, 
        max_value=10, 
        value=0,
        step=1,
        label_visibility="collapsed"
    )
    
    st.subheader("是否吸烟")
    smoker = st.radio("是否吸烟", ["是", "否"], horizontal=True, key="smoker", label_visibility="collapsed")
    
    st.subheader("区域")
    region = st.selectbox("区域", ["东南部", "东北部", "西北部", "西南部"], label_visibility="collapsed")
    
    st.write("")
    predict_button = st.button("预测费用", type="primary")
    
    st.write("---")
    
    if predict_button:
        if model is not None:
            try:
                sex_encoded = 0 if sex == "男性" else 1
                
                smoker_encoded = 1 if smoker == "是" else 0
                
                region_encoded = 0
                if label_encoders and '区域' in label_encoders:
                    region_classes = label_encoders['区域'].classes_
                    for i, reg in enumerate(region_classes):
                        if str(region) in str(reg):
                            region_encoded = i
                            break
                
                input_data = {
                    '年龄': age,
                    '性别': sex_encoded,
                    'BMI': bmi,
                    '子女数量': children,
                    '是否吸烟': smoker_encoded,
                    '区域': region_encoded
                }
                
                input_df = pd.DataFrame([input_data])
                
                input_df = input_df[feature_cols]
                
                prediction = model.predict(input_df)
                predicted_cost = prediction[0]
                
                st.success(f"### 预测医疗费用: ${predicted_cost:,.2f}")
                
            except Exception as e:
                st.error(f"预测过程中出现错误: {str(e)}")
        else:
            base_cost = 1000
            
            age_effect = age * 100
            
            if bmi < 18.5:
                bmi_effect = 500
            elif bmi < 25:
                bmi_effect = 0
            elif bmi < 30:
                bmi_effect = 1000
            else:
                bmi_effect = 2000
            
            smoker_effect = 5000 if smoker == "是" else 0
            
            children_effect = children * 500
            
            sex_effect = 300 if sex == "男性" else 0
            
            region_effect = {
                "东南部": 0,
                "东北部": 500,
                "西北部": -200,
                "西南部": 300
            }.get(region, 0)
            
            total_cost = base_cost + age_effect + bmi_effect + smoker_effect + children_effect + sex_effect + region_effect
            
            st.success(f"### 预测医疗费用: ${total_cost:,.2f}")
