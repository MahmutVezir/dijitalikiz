"""Independent public-API reproducer for NumPyro issue #1916.

This intentionally mirrors the reporter's warmup-then-run sequence. It does
not import or execute the upstream PR's regression test module.
"""
import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
from numpyro.infer import AIES, MCMC


def model(mu, sigma):
    with numpyro.plate("n_dim", 5):
        numpyro.sample("x", dist.Normal(mu, sigma))


def test_issue_1916_warmup_then_run_vectorized_aies():
    n_dim = 5
    num_chains = 100
    mu, sigma = jnp.zeros(n_dim), jnp.ones(n_dim)

    kernel = AIES(
        model,
        moves={
            AIES.DEMove(): 0.5,
            AIES.StretchMove(): 0.5,
        },
    )
    mcmc = MCMC(
        kernel,
        num_warmup=100,
        num_samples=100,
        num_chains=num_chains,
        chain_method="vectorized",
        progress_bar=False,
    )

    mcmc.warmup(jax.random.PRNGKey(0), mu, sigma)
    mcmc.run(jax.random.PRNGKey(1), mu, sigma)

    samples = mcmc.get_samples()
    assert "x" in samples
    assert samples["x"].shape[-1] == n_dim
