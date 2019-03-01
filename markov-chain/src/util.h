// Copyright 2019 Anthony Mirand.  All rights reserved
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef SRC_UTIL_H_
#define SRC_UTIL_H_

#include <fstream>
#include <random>
#include <string>
#include <vector>

#include "absl/strings/str_split.h"

namespace util {

template <typename Iter>
size_t HashContainer(const Iter begin, const Iter end) {
  typedef typename std::iterator_traits<Iter>::value_type T;
  const int distance = std::distance(begin, end);
  size_t seed = distance * (0 < distance ? begin->length() : 1);
  for (auto it = begin; it != end; it++) {
    seed ^= absl::Hash<T>{}(*it) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
  }
  return seed;
}

template <typename T>
T RandomNumberGenerator(const T min, const T max) {
  std::mt19937 rng;
  rng.seed(std::random_device()());
  std::uniform_real_distribution<T> distribution(min, max);
  return static_cast<T>(distribution(rng));
}

template<>
int RandomNumberGenerator(const int min, const int max) {
  std::mt19937 rng;
  rng.seed(std::random_device()());
  std::uniform_int_distribution<int> distribution(min, max);
  return static_cast<int>(distribution(rng));
}

std::vector<std::string> ReadFile(const std::string& filename) {
  std::ifstream infile{filename};
  std::string contents{std::istreambuf_iterator<char>(infile),
                       std::istreambuf_iterator<char>()};
  return absl::StrSplit(contents, absl::ByAnyChar(". \n"), absl::SkipEmpty());
}

}  // namespace util

#endif  // SRC_UTIL_H_
