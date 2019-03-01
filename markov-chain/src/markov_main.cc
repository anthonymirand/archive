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

#include <ctime>
#include <iostream>
#include <string>
#include <vector>

#include "../src/markov.h"
#include "../src/util.h"

int main(int argc, const char** argv) {
  const std::string filename = "data/rupi_kaur_corpus.txt";
  // const std::string filename = "data/stray_birds_corpus.txt";
  // const std::string filename = "data/shakespeare_sonnet_corpus.txt";

  clock_t begin_read = std::clock();
  const auto contents = util::ReadFile(filename);
  clock_t end_read = clock();
  const double elapsed_secs_read =
      double(end_read - begin_read) / CLOCKS_PER_SEC;

  markov::Markov<absl::string_view> chain(2);

  clock_t begin_data = std::clock();
  chain.AddData(contents.begin(), contents.end());
  clock_t end_data = clock();
  const double elapsed_secs_data =
      double(end_data - begin_data) / CLOCKS_PER_SEC;

  // if (DEBUG) std::cout << chain.DebugString();

  clock_t begin_gen = std::clock();
  const int num_poems = 10, poem_length = 25;
  std::cout << "\n\n";
  for (int i = 0; i < num_poems; i++) {
    std::string text = chain.Generate(poem_length);
    std::cout << text << "\n\n";
  } std::cout << "\n";
  clock_t end_gen = clock();
  const double elapsed_secs_gen =
      double(end_gen - begin_gen) / (num_poems * CLOCKS_PER_SEC);

  std::cout << "Read file:\t" << elapsed_secs_read << "\n";
  std::cout << "Data add:\t" << elapsed_secs_data << "\n";
  std::cout << "Avg poem:\t" << elapsed_secs_gen << "\n\n";

  return 0;
}
