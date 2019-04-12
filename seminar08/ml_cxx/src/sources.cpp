#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <vector>
#include <random>
#include <future>

namespace py = pybind11;

std::vector<double> func(int seed, int size) {
  std::mt19937 engine(seed);
  std::uniform_int_distribution<int> rand_val(0, 1);
  std::vector<double> result;
  result.reserve(size);
  for (int iter = 0; iter < size; ++iter) {
    int sum = 0;
    for (int sample = 0; sample < 10000; ++sample) {
      sum += rand_val(engine) * 2 - 1;
    }
    result.push_back(sum / 10000.);
  }
  return result;
}

std::vector<double> async_func(int seed, int size, int n_jobs) {
  std::vector<std::future<std::vector<double>>> distributions;
  const int task_size = (size + n_jobs - 1) / n_jobs;
  for (int iter_start = 0; iter_start < size;
       iter_start += task_size) {
    int batch_size = std::min(size, iter_start + task_size) - iter_start;
    distributions.emplace_back(std::async(
        std::launch::async,
        func, seed + iter_start, batch_size
    ));
  }

  std::vector<double> result;
  for (auto& async_batch : distributions) {
    const auto batch = async_batch.get();
    result.insert(
        result.end(), batch.begin(), batch.end()
    );
  }
  return result;
}

py::array_t<double> py_func(int n_jobs = 1) {
  std::vector<double> result;
  if (n_jobs == 1) {
    result = func(42, 10000);
  } else {
    result = async_func(42, 10000, n_jobs);
  }
  return py::array_t<double>(result.size(), result.data());
}

PYBIND11_MODULE(ml_cxx, ml_cxx) {
  ml_cxx.def("func", &py_func, py::arg("n_jobs") = 1);
}
