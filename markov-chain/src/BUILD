# Copyright 2019 Anthony Mirand.  All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cc_library(
  name = "state",
  hdrs = ["state.h"],
  deps = [
    ":util",
    "@com_google_absl//absl/container:flat_hash_map",
    "@com_google_absl//absl/strings",
  ],
)

cc_library(
  name = "markov",
  hdrs = ["markov.h"],
  deps = [
    ":state",
    "@com_google_absl//absl/container:flat_hash_map",
    "@com_google_absl//absl/strings",
  ],
)

cc_binary(
  name = "markov_main",
  srcs = ["markov_main.cc"],
  data = [
    "//data:rupi_kaur_corpus.txt",
    "//data:shakespeare_sonnet_corpus.txt",
    "//data:stray_birds_corpus.txt",
  ],
  deps = [
    ":markov",
  ],
)

cc_library(
  name = "util",
  hdrs = ["util.h"],
  deps = [
    "@com_google_absl//absl/strings",
  ],
)
