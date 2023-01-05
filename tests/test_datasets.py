import pytest
import torch

def test_dataset_size(generated_dataset):
    assert len(generated_dataset) == 10

def test_normal_params(generated_normal_dataset):
    from torch.testing import assert_close
    from torch import mean, std
    for data in generated_normal_dataset:
        samples = data.W0[data.W0 != 0]
        assert_close(mean(samples), torch.tensor(0.0), atol=5e-2, rtol=5e-2)
        assert_close(std(samples), torch.tensor(1.0), atol=5e-2, rtol=5e-2)

def test_consistent_datasets(saved_dataset, generated_dataset):
    from torch.testing import assert_close
    for i in range(len(saved_dataset)):
        s = saved_dataset[i]
        g = generated_dataset[i]
        assert_close(s.W0, g.W0)
        assert_close(s.edge_index, g.edge_index)
        assert s.num_nodes == g.num_nodes

def test_numpy_dataset():
    from spiking_network.datasets import ConnectivityDataset
    import shutil
    dataset = ConnectivityDataset(root="tests/test_data/numpy_dataset")
    shutil.rmtree("tests/test_data/numpy_dataset/processed")
    assert len(dataset) == 10
    assert dataset[0].W0.dtype == torch.float32
    assert dataset[0].edge_index.dtype == torch.int64

def test_fails_for_odd_number_of_neurons():
    from spiking_network.datasets import W0Dataset, GlorotParams
    with pytest.raises(ValueError):
        W0Dataset(21, 10, GlorotParams(0, 5), root="")

def test_fails_for_negative_number_of_sims():
    from spiking_network.datasets import W0Dataset, GlorotParams
    with pytest.raises(ValueError):
        W0Dataset(10, -1, GlorotParams(0, 5), root="")

def test_to_dense(saved_dataset):
    from torch import sparse_coo_tensor
    from torch.testing import assert_close
    dense_data = saved_dataset.to_dense()[0]
    w0 = saved_dataset[0].W0
    edge_index = saved_dataset[0].edge_index
    sparse_data = sparse_coo_tensor(edge_index, w0, dense_data.shape)
    assert_close(dense_data, sparse_data.to_dense())
    
def test_number_of_neurons_in_dataset(generated_dataset):
    assert all([data.num_nodes == 20 for data in generated_dataset])

def test_self_loops_in_dataset(generated_dataset):
    assert all([data.has_self_loops() for data in generated_dataset])

def test_mexican_hat_dataset(generated_mexican_hat_dataset):
    assert len(generated_mexican_hat_dataset) == 10
    assert all([data.num_nodes == 20 for data in generated_mexican_hat_dataset])
    assert all([data.has_self_loops() for data in generated_mexican_hat_dataset])

def test_sparse_dataset(generated_dataset, sparse_dataset):
    from spiking_network.datasets import W0Dataset, GlorotParams
    assert not torch.equal(sparse_dataset[0].W0, generated_dataset[0].W0)
    assert sparse_dataset[0].W0.numel() < generated_dataset[0].W0.numel()

def test_generate_examples(saved_dataset):
    from spiking_network.datasets import W0Dataset, GlorotParams
    from torch.testing import assert_close
    data = W0Dataset.generate_examples(20, 10, GlorotParams(0, 5), seed=0)
    for i in range(len(data)):
        assert_close(data[i].W0, saved_dataset[i].W0)
        assert_close(data[i].edge_index, saved_dataset[i].edge_index)