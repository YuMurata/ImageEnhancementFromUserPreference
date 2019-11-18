#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Jupyter'))
	print(os.getcwd())
except:
	pass
#%% [markdown]
# # 画像の収集
# 1. ' TrainData ' 以下のフォルダに入る
# 2. 任意のフォルダで ' googleimagesdownload -k _KEYWORD_ -l 5 ' を実行する
#
#     [参考ページ](https://co.bsnws.net/article/295)
#

#%%
from pathlib import Path

TrainData_path = Path('C:\\Users\\init\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\TrainData')
image_dir_path = TrainData_path/'Photography'/'Artificial'

keyword = 'salad'
dl_num = 3


#%%
get_ipython().run_line_magic('cd', '$str(image_dir_path)')
get_ipython().system('googleimagesdownload -k $keyword -l $dl_num -o ./')


#%%
import shutil

downloaded_path = image_dir_path/keyword
image_path_list = list(downloaded_path.iterdir())

folder_index_list = [i+1 for i in range(dl_num)]
folder_path_list = []
for folder_index in folder_index_list:
    folder_path = downloaded_path/str(folder_index)
    if not folder_path.exists():
        folder_path.mkdir()
    folder_path_list.append(folder_path)


for folder_path, image_path in zip(folder_path_list, image_path_list):
    shutil.move(str(image_path), str(folder_path)+'/')



#%% [markdown]
# # 学習データを作る
#%% [markdown]
# ## スコアをつける

#%%
get_ipython().run_line_magic('run', '-i C:\\Users\\init\\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\TrainDataGenerator\\tournament_comparer.py')

#%% [markdown]
# ## スコアデータのグラフ化
# グラフは ' 研究成果/画像/_カテゴリ_/グラフ ' に保存する

#%%
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('run', '-i C:\\Users\\init\\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\TrainDataGenerator\\param_score_graphizer.py')

#%% [markdown]
# ### モデルタイプの選択

#%%
model_type = 'compare'

#%% [markdown]
# ## スコアデータからTFRecords形式へ変換

#%%
get_ipython().run_line_magic('run', '-i C:\\Users\\init\\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\TrainDataGenerator\\TFRecordsMaker\\ScoredParamConverter\\scored_param_converter.py $model_type')

#%% [markdown]
# # 好みの学習
#%% [markdown]
# ## 学習

#%%
get_ipython().run_line_magic('run', '-i C:\\Users\\init\\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\UserPreferencePredictor\\predictor_trainer.py $model_type')

#%% [markdown]
# ## 評価値高い順に並び替え
# 出力は ' 研究成果/画像/_カテゴリ_/評価値とスコアの比較 ' に保存する

#%%
get_ipython().run_line_magic('run', '-i C:\\Users\\init\\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\UserPreferencePredictor\\evaluate_visualizer.py $model_type')

#%% [markdown]
# # 最適化
# 出力は ' 研究成果/画像/_カテゴリ_/最適化 ' に保存する

#%%
get_ipython().run_line_magic('run', '-i C:\\Users\\init\\Documents\\PythonScripts\\PredictEvaluationFromHumanPreference\\ParameterOptimizer\\parameter_optimizer.py $model_type')


