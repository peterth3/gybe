"""Kubernetes models as dataclasses copied from k8s' OpenAPI V3 Spec."""

from gybe.k8s.types import K8sSpec, K8sResource
from gybe.k8s.v1_30.apps.v1 import (
    DaemonSet,
    DaemonSetSpec,
    Deployment,
    DeploymentSpec,
    DeploymentStrategy,
    StatefulSet,
    StatefulSetSpec,
)
from gybe.k8s.v1_30.batch.v1 import Job, JobSpec
from gybe.k8s.v1_30.core.v1 import (
    Affinity,
    Container,
    ContainerPort,
    EnvFromSource,
    EnvVar,
    EnvVarSource,
    HTTPGetAction,
    ObjectFieldSelector,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeSpec,
    Pod,
    PodAffinityTerm,
    PodAntiAffinity,
    PodSpec,
    PodTemplateSpec,
    Probe,
    ResourceRequirements,
    Secret,
    SecretEnvSource,
    SecretKeySelector,
    SecretVolumeSource,
    SecurityContext,
    Service,
    ServicePort,
    ServiceSpec,
    Volume,
    VolumeMount,
    VolumeResourceRequirements,
    WeightedPodAffinityTerm,
)
from gybe.k8s.v1_30.meta.v1 import LabelSelector, LabelSelectorRequirement, ObjectMeta
from gybe.k8s.v1_30.networking.v1 import (
    Ingress,
    IngressBackend,
    IngressServiceBackend,
    IngressSpec,
    ServiceBackendPort,
)

__all__ = [
    'Affinity',
    'Container',
    'ContainerPort',
    'DaemonSet',
    'DaemonSetSpec',
    'Deployment',
    'DeploymentSpec',
    'DeploymentStrategy',
    'EnvFromSource',
    'EnvVar',
    'EnvVarSource',
    'HTTPGetAction',
    'Ingress',
    'IngressBackend',
    'IngressServiceBackend',
    'IngressServiceBackendPort',
    'IngressSpec',
    'Job',
    'JobSpec',
    'K8sResource',
    'K8sSpec',
    'LabelSelector',
    'LabelSelectorRequirement',
    'ObjectFieldSelector',
    'ObjectMeta',
    'PersistentVolume',
    'PersistentVolumeClaim',
    'PersistentVolumeClaimSpec',
    'PersistentVolumeClaimSpec',
    'PersistentVolumeSpec',
    'Pod',
    'PodAffinityTerm',
    'PodAntiAffinity',
    'PodSpec',
    'PodTemplateSpec',
    'Probe',
    'ResourceRequirements',
    'Secret',
    'SecretEnvSource',
    'SecretKeySelector',
    'SecretVolumeSource',
    'SecurityContext',
    'Service',
    'ServiceBackendPort',
    'ServicePort',
    'ServiceSpec',
    'StatefulSet',
    'StatefulSetSpec',
    'Volume',
    'VolumeMount',
    'VolumeResourceRequirements',
    'WeightedPodAffinityTerm',
]
