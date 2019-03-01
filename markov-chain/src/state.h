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

#ifndef SRC_STATE_H_
#define SRC_STATE_H_

#include <deque>
#include <memory>
#include <string>
#include <utility>

#include "absl/container/flat_hash_map.h"
#include "absl/strings/str_cat.h"
#include "../src/util.h"

namespace state {

template <typename T>
class State {
 public:
  explicit State(std::deque<T> data);
  T GetData();
  std::deque<T> GetAllData();
  State<T>* GetNextState();
  void AddTransition(State<T>* next_state);
  std::string DebugString();

 private:
  std::deque<T> data_;
  absl::flat_hash_map<State<T>*, int> transitions_;
};

template <typename T>
State<T>::State(std::deque<T> data) :
    data_(data) {}

template <typename T>
T State<T>::GetData() {
  return data_.back();
}

template <typename T>
std::deque<T> State<T>::GetAllData() {
  return data_;
}

// #include <iostream>
template <typename T>
State<T>* State<T>::GetNextState() {
  if (transitions_.empty()) {
    return nullptr;
  }
  const auto lambda = [](const int& a,
                         const std::pair<State<T>*, int>& b){
      return a + b.second; };
  const int total = std::accumulate(
      transitions_.begin(), transitions_.end(), 0, lambda);
  int random_weight = util::RandomNumberGenerator(0, total);
  for (const auto& transition : transitions_) {
    random_weight -= transition.second;
    if (random_weight <= 0) {
      return transition.first;
    }
  }
  assert("Incorrectly selecting next state");
  return nullptr;
}

template <typename T>
void State<T>::AddTransition(State<T>* next_state) {
  transitions_[next_state]++;
}

template<typename T>
std::string State<T>::DebugString() {
  std::string result = "(", terminal = "";
  for (const auto& data : data_) {
    terminal = (data == data_.back()) ? "" : ",";
    absl::StrAppend(&result, "\"", data, "\"", terminal);
  } absl::StrAppend(&result, ")  :  [");
  for (const auto& transition : transitions_) {
    absl::StrAppend(&result, "{(");
    for (const auto& key : transition.first->GetAllData()) {
      terminal = (key == transition.first->GetAllData().back()) ? "" : ",";
      absl::StrAppend(&result, "\"", key, "\"", terminal);
    }
    absl::StrAppend(&result, ") : ", transition.second, "},");
  } absl::StrAppend(&result, "]\n");
  return result;
}

}  // namespace state

#endif  // SRC_STATE_H_
