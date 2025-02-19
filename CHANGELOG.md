# Change Log

## Unreleased

### Added

- Add PyTorch nn Module wrapper in `torchnn`

## 0.1.3

### Added

- Add more type auto conversion for `tc.gates.Gate` as inputs

- Add `tree_flatten` and `tree_unflatten` method on backends

- Add torch optimizer to the backend agnostic optimizer abstraction

### Changed

- Refactor the tree utils, add native torch support for pytree utils

### Fixed

- grad in torch backend now support pytrees

- fix float parameter issue in translation to qiskit circuit (#19)

## 0.1.2

### Added

- Add `rxx`, `ryy` and `rzz` gate

### Fixed

- Fix installation issue with tensorflow requirements on MACOS with M1 chip

- Improve M1 macOS compatibility with unjit tensorflow ops

- Fixed SVD backprop bug on jax backend of wide matrix

- `mps_input` dtype auto correction enabled

## 0.1.1

### Added

- Add `quoperator` method to get `QuOperator` representation of the circuit unitary

- Add `coo_sparse_matrix_from_numpy` method on backend, where the scipy coo matrix is converted to sparse tensor in corresponding backend

- Add sparse tensor to scipy coo matrix implementation in `numpy` method

### Changed

- `tc.quantum.PauliStringSum2COO`, `tc.quantum.PauliStringSum2Dense`, and `tc.quantum.heisenberg_hamiltonian` now return the tensor in current backend format if `numpy` option sets to False. (Breaking change: previously, the return are fixed in TensorFlow format)

## 0.1.0

### Added

- `DMCircuit` also supports array instead of gate as the operator

### Fixed

- fix translation issue to qiskit when the input parameter is in numpy form

- type conversion in measure API when high precision is set

- fix bug in to_qiskit with new version qiskit

## 0.0.220509

### Added

- Add `eigvalsh` method on backend

### Changed

- `post_select` method return the measurement result int tensor now, consistent with `cond_measure`

- `Circuit.measure` now point to `measure_jit`

## 0.0.220413

### Added

- Add `expectation_ps` method for `DMCircuit`

- Add `measure` and `sample` for `DMCircuit`

### Fixed

- With `Circuit.vis_tex`, for the Circuit has customized input state, the default visualization is psi instead of all zeros now

- `general_kraus` is synced with `apply_general_kraus` for `DMCircuit`

- Fix dtype incompatible issue in kraus methods between status and prob

## 0.0.220402

### Added

- add `utils.append` to build function pipeline

- add `mean` method on backends

- add trigonometric methods on backends

- add `conditional_gate` to support quantum ops based on previous measurment results

- add `expectation_ps` as shortcut to get Pauli string expectation

- add `append` and `prepend` to compose circuits

- add `matrix` method to get the circuit unitary matrix

### Changed

- change the return information of `unitary_kraus` and `general_kraus` methods

- add alias for any gate as unitary

## 0.0.220328

### Added

- add QuOperator convert tools which can convert MPO in the form of TensorNetwork and Quimb into MPO in the form of QuOperator

### Changed

- quantum Hamiltonian generation now support the direct return of numpy form matrix

### Fixed

- unitary_kraus and general_kraus API now supports the mix input of array and Node as kraus list

## 0.0.220318

### Added

- add gradient free scipy interface for optimization

- add qiskit circuit to tensorcircuit circuit methods

- add draw method on circuit from qiskit transform pipeline

### Changed

- futher refactor VQNHE code in applications

- add alias `sample` for `perfect_sampling` method

- optimize VQNHE pipeline for a more stable training loop (breaking changes in some APIs)

### Fixed

- Circuit inputs will convert to tensor first

## 0.0.220311

### Added

- add sigmoid method on backends

- add MPO expectation template function for MPO evaluation on circuit

- add `operator_expectation` in templates.measurements for a unified expectation interface

- add `templates.chems` module for interface between tc and openfermion on quantum chemistry related tasks

- add tc.Circuit to Qiskit QuantumCircuit transformation

### Fixed

- fix the bug in QuOperator.from_local_tensor where the dtype should always be in numpy context

- fix MPO copy when apply MPO gate on the circuit

### Changed

- allow multi-qubit gate in multicontrol gate

## 0.0.220301

### Added

- new universal contraction analyse tools and pseudo contraction rehearsals for debug

- add `gather1d` method on backends for 1d tensor indexing

- add `dataset` module in template submodule for dataset preprocessing and embedding

- MPO format quantum gate is natively support now

- add multicontrol gates in MPO format

### Fixed

- fixed real operation on some methods in templates.measurements

### Changed

- add gatef key in circuit IR dict for the gate function, while replace gate key with the gate node or MPO (breaking change)

## 0.0.220126

### Added

- add `td` and `sd` gates for dagger version of T gate and S gate

- add `argmax` and `argmin` as backend methods

- add `expectation_before` methods for `tc.Circuit` for further manipulation on the tensornetwork

### Changed

- refined repr for `tc.gates.Gate`

- expectation API now supports int index besides list indexes

### Fixed

- make consistent `Gate` return for channels

- fixed bug on list optimizer for contraction

- stability for QR operator in terms of automatic differentiation

## 0.0.220118

### Added

- add `hessian` method on backends

- add further automatic pipelines for visualization by generating pdf or images

- add `reshape2` method on backends as a short cut to reshape a tensor with all legs 2-d

- add `reshapem` method on backends to reshape any tensor as a square matrix

- add `controlled` and `ocontrolled` API to generate more gates

- add `crx`, `cry`, `crz` gate on `Circuit`

- add `__repr__` and `__str__` for backend object

- `tc.expectation` now support ket arg as quvector form

### Fixed

- `sizen` correctly returns 1 for tensor of no shape

- fixed `convert_to_tensor` bug in numpy backend in TensorNetwork

- `any_gate` also support Gate format instead of matrix

- `matrix_for_gate` works now for backends more than numpy

### Changed

- `expectation` API now also accepts plain tensor instead of `tc.Gate`.

- `DMCircuit` and `DMCircuit2` are all pointing the efficent implementations (breaking changes)

## 0.0.220106

### Added

- add `solve` method on backends to solve linear equations

- add full quantum natural gradient examples and `qng` method in experimental module

- add `concat` method to backends

- add `stop_gradient` method to backends

- add `has_aux` arg on `vvag` method

- add `imag` method on backends

- add `Circuit.vis_tex` interface that returns the quantikz circuit latex

### Changed

- contractor, dtype and backend set are default to return objects, `with tc.runtime_backend("jax") as K` or `K = tc.set_backend("jax")` could work

- change `perfect_sampling` to use `measure_jit` behind the scene

- `anygate` automatically reshape the unitary input to 2-d leg for users' good

- `quantum.renyi_entropy` computation with correct prefactor

- `Circuit` gate can provided other names by name attr

- `example_block` support param auto reshape for users' good

### Fixed

- make four algorithms for quantum natural gradient consistent and correct

- torch `real` is now a real

## 0.0.211223

### Added

- add `quantum.heisenberg_hamiltonian` for hamiltonian generation shortcut

- add `has_aux` parameter in backend methods `grad` and `value_and_grad`, the semantic syntax is the same as jax

- add `optimizer` class on tensorflow and jax backend, so that a minimal and unified backend agnostic optimizer interface is provided

- add `quantum.mutual_information`, add support on mixed state for `quantum.reduced_density_matrix`

- add `jvp` methods for tensorflow, jax, torch backends, and ensure pytree support in `jvp` and `vjp` interfaces for tensorflow and jax backends; also ensure complex support for `jvp` and `vjp`

- add `jacfwd` and `jacrev` for backend methods (experimental API, may have bugs and subject to changes)

### Fixed

- fix `matmul` bug on tensornetwork tensorflow backend

### Changed

- delete `qcode` IR for `Circuit`, use `qir` instead (breaking changes)

- basic circuit running is ok on pytorch backend with some complex support fixing

## 0.0.211216

### Added

- add `get_random_state` and `random_split` methods to backends

- add qir representation of circuit, `c.to_qir()` and `Circuit.from_qir()` methods

- fine-grained control on backend, dtype and contractor setup: `tc.set_function_backend()` for function level decorator and `tc.runtime_backend()` as with context manager

- add `state_centric` decorator in `tc.templates.blocks` to transform circuit-to-circuit funtion to state-to-state function

- add `interfaces.scipy_optimize_interface` to transform quantum function into `scipy.optimize.minimize` campatible form

### Fixed

- avoid error on watch non `tf.Tensor` in tensorflow backend grad method

- circuit preprocessing simplification with only single qubit gates

- avoid the bug when random from jax backend with jitted function

- refresh the state cache in Circuit when new gate is applied

### Changed

- refactor `tc.gates` (breaking API on `rgate` -> `r_gate`, `iswapgate` -> `iswap_gate`)
