"""
Loss submodule.

This submodule contains the various losses used in CAREamics.
"""
from typing import Type

import torch
from torch.nn import L1Loss

from .noise_models import HistogramNoiseModel


def n2v_loss(
    samples: torch.Tensor, labels: torch.Tensor, masks: torch.Tensor
) -> torch.Tensor:
    """
    N2V Loss function described in A Krull et al 2018.

    Parameters
    ----------
    samples : torch.Tensor
        Patches with manipulated pixels.
    labels : torch.Tensor
        Noisy patches.
    masks : torch.Tensor
        Array containing masked pixel locations.

    Returns
    -------
    torch.Tensor
        Loss value.
    """
    errors = (labels - samples) ** 2
    # Average over pixels and batch
    loss = torch.sum(errors * masks) / torch.sum(masks)
    return loss


def n2n_loss(samples: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    """
    N2N Loss function described in to J Lehtinen et al 2018.

    Parameters
    ----------
    samples : torch.Tensor
        Raw patches.
    labels : torch.Tensor
        Different subset of noisy patches.

    Returns
    -------
    torch.Tensor
        Loss value.
    """
    loss = L1Loss()
    return loss(samples, labels)


def pn2v_loss(
    samples: torch.Tensor,
    labels: torch.Tensor,
    masks: torch.Tensor,
    noise_model: Type[HistogramNoiseModel],
):
    """Probabilistic N2V loss function described in A Krull et al 2019."""
    likelihoods = noise_model.likelihood(labels, samples)
    likelihoods_avg = torch.log(torch.mean(likelihoods, dim=0, keepdim=True)[0, ...])

    # Average over pixels and batch
    loss = -torch.sum(likelihoods_avg * masks) / torch.sum(masks)
    return loss
