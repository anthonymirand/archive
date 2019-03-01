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

#ifndef SRC_MARKOV_H_
#define SRC_MARKOV_H_

#include <deque>
#include <memory>
#include <string>
#include <vector>

#include "absl/container/flat_hash_map.h"
#include "absl/strings/str_cat.h"
#include "../src/state.h"
#include "../src/util.h"

namespace markov {

template <typename T>
class State;

template <typename T>
class Markov {
 public:
  explicit Markov(const int chain_size = 1);
  template <typename Iter> void AddData(const Iter begin, const Iter end);
  std::string Generate(const int length);
  std::string DebugString();

 private:
  T GetData();
  void Init();
  bool Advance();

  int chain_size_;
  state::State<T>* current_state_ = nullptr;
  absl::flat_hash_map<size_t, std::unique_ptr<state::State<T>>> states_;
};

template <typename T>
Markov<T>::Markov(const int chain_size) :
    chain_size_(chain_size) {}

template <typename T>
T Markov<T>::GetData() {
  return current_state_->GetData();
}

template <typename T>
void Markov<T>::Init() {
  const int max_index = states_.size() - 1;
  const int random = util::RandomNumberGenerator(0, max_index);
  auto it = states_.begin();
  std::advance(it, random);
  current_state_ = it->second.get();
}

template <typename T>
template <typename Iter>
void Markov<T>::AddData(const Iter begin, const Iter end) {
  std::deque<T> data{begin, begin + chain_size_};
  data.push_front(NULL); data.pop_back();
  for (auto it = begin; it != end - chain_size_ + 1; it++) {
    const auto it_data = it + chain_size_;
    data.pop_front(); data.push_back(*it_data);
    const auto hash = util::HashContainer(data.begin(), data.end());

    state::State<T>* state;
    const auto it_ = states_.find(hash);
    if (it_ != states_.end()) {
      state = it_->second.get();
    } else {
      states_.insert({hash, absl::make_unique<state::State<T>>(data)});
      state = states_[hash].get();
    }
    if (current_state_ != nullptr) {
      current_state_->AddTransition(state);
    }
    current_state_ = state;
  }
}

template <typename T>
bool Markov<T>::Advance() {
  const auto next_state = current_state_->GetNextState();
  if (next_state == nullptr) {
    return false;
  }
  current_state_ = next_state;
  return true;
}

template <typename T>
std::string Markov<T>::Generate(const int length) {
  Init();
  std::string result = "";
  for (int i = 0; i < length; i++) {
    absl::StrAppend(&result, GetData(), " ");
    if (!Advance()) break;
  }
  return result;
}

template<typename T>
std::string Markov<T>::DebugString() {
  std::string result = "";
  for (const auto& state : states_) {
    absl::StrAppend(&result, state.second->DebugString());
  }
  return result;
}

}  // namespace markov

#endif  // SRC_MARKOV_H_
