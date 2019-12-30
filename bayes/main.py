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
	with pm.Model() as model_10:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_10)
	with model_10:
		start = pm.find_MAP()
		step = pm.NUTS()
		trace = pm.sample(2000, step, start)
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
		trace = pm.sample(5000, step, start)
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
		trace = pm.sample(10000, step, start)
	print(pm.traceplot(trace))
	plt.savefig('result_10B')


def sample100():
	print('----------100')
	with pm.Model() as model_100:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_100)
	with model_100:
		start = pm.find_MAP()
		step = pm.NUTS()
		trace = pm.sample(2000, step, start)
	print(pm.traceplot(trace))
	plt.savefig('result_100')


def sample1000():
	print('---------1000')
	with pm.Model() as model_1000:
		mu = pm.Normal('mu', mu=0., sd=0.1)
		x = pm.Normal('x', mu=mu, sd=1., observed=x_sample_1000)
	with model_1000:
		start = pm.find_MAP()
		step = pm.NUTS()
		trace = pm.sample(2000, step, start)
	print(pm.traceplot(trace))
	plt.savefig('result_1000')


def main():
	sample10()
	sample10A()
	sample10B()
	# sample100()
	# sample1000()
	

if __name__ == '__main__':
    print('main---start')
    main()
