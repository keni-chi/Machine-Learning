import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt


print('----------000')
x_sample_10 = np.random.normal(loc=1.0, scale=1.0, size=10)
x_sample_100 = np.random.normal(loc=1.0, scale=1.0, size=100)
x_sample_1000 = np.random.normal(loc=1.0, scale=1.0, size=1000)
print(x_sample_10)
print(np.mean(x_sample_10))


def sample10():
	print('----------010')
	# 単純なガウス分布の平均パラメータの推定
	with pm.Model() as model_10:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		print('===001')
		print(mu)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_10)
		print('===002')
		print(x)
	with model_10:
		# サンプリングの初期値として、MAP推定の結果を利用
		start = pm.find_MAP()
		print('===003')
		print(start)
		# No-U-Turn Sampler の略。サンプリング手法。
		step = pm.NUTS()
		print('===004')
		print(step)
		# 100イテレーション
		trace = pm.sample(100, step, start)
		print('===005')
		print(trace)
	print('===006')
	print(pm.traceplot(trace))
	print(pm.summary(trace).round(2))
	plt.savefig('result_10')


def sample10A():
	print('----------010A')
	with pm.Model() as model_10:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_10)
	with model_10:
		start = pm.find_MAP()
		step = pm.NUTS()
		trace = pm.sample(200, step, start)
	print(pm.traceplot(trace))
	plt.savefig('result_10A')


def sample10B():
	print('----------010B')
	with pm.Model() as model_10:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_10)
	with model_10:
		start = pm.find_MAP()
		step = pm.NUTS()
		trace = pm.sample(300, step, start)
	print(pm.traceplot(trace))
	plt.savefig('result_10B')


def sample1000():
	print('----------010')
	# 単純なガウス分布の平均パラメータの推定
	with pm.Model() as model_10:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		print('===001')
		print(mu)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_1000)
		print('===002')
		print(x)
	with model_10:
		# サンプリングの初期値として、MAP推定の結果を利用
		start = pm.find_MAP()
		print('===003')
		print(start)
		# No-U-Turn Sampler の略。サンプリング手法。
		step = pm.NUTS()
		print('===004')
		print(step)
		# 100イテレーション
		trace = pm.sample(100, step, start)
		print('===005')
		print(trace)
	print('===006')
	print(pm.traceplot(trace))
	print(pm.summary(trace).round(2))
	plt.savefig('result_1000')


def main():
	sample10()
	sample10A()
	sample10B()
	sample1000()
	

if __name__ == '__main__':
    print('main---start')
    main()
