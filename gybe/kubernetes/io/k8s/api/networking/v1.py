from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from ...apimachinery.pkg.apis.meta import v1 as v1_1
from ...apimachinery.pkg.util import intstr
from ..core import v1


class IPBlock(BaseModel):
    cidr: str = Field(
        ...,
        description=(
            "cidr is a string representing the IPBlock Valid examples are"
            ' "192.168.1.0/24" or "2001:db8::/64"'
        ),
    )
    except_: Optional[List[str]] = Field(
        None,
        alias="except",
        description=(
            "except is a slice of CIDRs that should not be included within an IPBlock"
            ' Valid examples are "192.168.1.0/24" or "2001:db8::/64" Except values will'
            " be rejected if they are outside the cidr range"
        ),
    )


class IngressClassParametersReference(BaseModel):
    apiGroup: Optional[str] = Field(
        None,
        description=(
            "apiGroup is the group for the resource being referenced. If APIGroup is"
            " not specified, the specified Kind must be in the core API group. For any"
            " other third-party types, APIGroup is required."
        ),
    )
    kind: str = Field(..., description="kind is the type of resource being referenced.")
    name: str = Field(..., description="name is the name of resource being referenced.")
    namespace: Optional[str] = Field(
        None,
        description=(
            "namespace is the namespace of the resource being referenced. This field is"
            ' required when scope is set to "Namespace" and must be unset when scope is'
            ' set to "Cluster".'
        ),
    )
    scope: Optional[str] = Field(
        None,
        description=(
            "scope represents if this refers to a cluster or namespace scoped resource."
            ' This may be set to "Cluster" (default) or "Namespace".'
        ),
    )


class IngressClassSpec(BaseModel):
    controller: Optional[str] = Field(
        None,
        description=(
            "controller refers to the name of the controller that should handle this"
            ' class. This allows for different "flavors" that are controlled by the'
            " same controller. For example, you may have different parameters for the"
            " same implementing controller. This should be specified as a"
            " domain-prefixed path no more than 250 characters in length, e.g."
            ' "acme.io/ingress-controller". This field is immutable.'
        ),
    )
    parameters: Optional[IngressClassParametersReference] = Field(
        None,
        description=(
            "parameters is a link to a custom resource containing additional"
            " configuration for the controller. This is optional if the controller does"
            " not require extra parameters."
        ),
    )


class IngressPortStatus(BaseModel):
    error: Optional[str] = Field(
        None,
        description=(
            "error is to record the problem with the service port The format of the"
            " error shall comply with the following rules: - built-in error values"
            " shall be specified in this file and those shall use\n  CamelCase names\n-"
            " cloud provider specific error values must have names that comply with"
            " the\n  format foo.example.com/CamelCase."
        ),
    )
    port: int = Field(..., description="port is the port number of the ingress port.")
    protocol: str = Field(
        ...,
        description=(
            "protocol is the protocol of the ingress port. The supported values are:"
            ' "TCP", "UDP", "SCTP"'
        ),
    )


class IngressTLS(BaseModel):
    hosts: Optional[List[str]] = Field(
        None,
        description=(
            "hosts is a list of hosts included in the TLS certificate. The values in"
            " this list must match the name/s used in the tlsSecret. Defaults to the"
            " wildcard host setting for the loadbalancer controller fulfilling this"
            " Ingress, if left unspecified."
        ),
    )
    secretName: Optional[str] = Field(
        None,
        description=(
            "secretName is the name of the secret used to terminate TLS traffic on port"
            " 443. Field is left optional to allow TLS routing based on SNI hostname"
            ' alone. If the SNI host in a listener conflicts with the "Host" header'
            " field used by an IngressRule, the SNI host is used for termination and"
            ' value of the "Host" header is used for routing.'
        ),
    )


class ServiceBackendPort(BaseModel):
    name: Optional[str] = Field(
        None,
        description=(
            "name is the name of the port on the Service. This is a mutually exclusive"
            ' setting with "Number".'
        ),
    )
    number: Optional[int] = Field(
        None,
        description=(
            "number is the numerical port number (e.g. 80) on the Service. This is a"
            ' mutually exclusive setting with "Name".'
        ),
    )


class IngressLoadBalancerIngress(BaseModel):
    hostname: Optional[str] = Field(
        None,
        description=(
            "hostname is set for load-balancer ingress points that are DNS based."
        ),
    )
    ip: Optional[str] = Field(
        None,
        description="ip is set for load-balancer ingress points that are IP based.",
    )
    ports: Optional[List[IngressPortStatus]] = Field(
        None,
        description=(
            "ports provides information about the ports exposed by this LoadBalancer."
        ),
    )


class IngressLoadBalancerStatus(BaseModel):
    ingress: Optional[List[IngressLoadBalancerIngress]] = Field(
        None,
        description=(
            "ingress is a list containing ingress points for the load-balancer."
        ),
    )


class IngressServiceBackend(BaseModel):
    name: str = Field(
        ...,
        description=(
            "name is the referenced service. The service must exist in the same"
            " namespace as the Ingress object."
        ),
    )
    port: Optional[ServiceBackendPort] = Field(
        None,
        description=(
            "port of the referenced service. A port name or port number is required for"
            " a IngressServiceBackend."
        ),
    )


class IngressStatus(BaseModel):
    loadBalancer: Optional[IngressLoadBalancerStatus] = Field(
        None,
        description="loadBalancer contains the current status of the load-balancer.",
    )


class NetworkPolicyPort(BaseModel):
    endPort: Optional[int] = Field(
        None,
        description=(
            "endPort indicates that the range of ports from port to endPort if set,"
            " inclusive, should be allowed by the policy. This field cannot be defined"
            " if the port field is not defined or if the port field is defined as a"
            " named (string) port. The endPort must be equal or greater than port."
        ),
    )
    port: Optional[intstr.IntOrString] = Field(
        None,
        description=(
            "port represents the port on the given protocol. This can either be a"
            " numerical or named port on a pod. If this field is not provided, this"
            " matches all port names and numbers. If present, only traffic on the"
            " specified protocol AND port will be matched."
        ),
    )
    protocol: Optional[str] = Field(
        None,
        description=(
            "protocol represents the protocol (TCP, UDP, or SCTP) which traffic must"
            " match. If not specified, this field defaults to TCP."
        ),
    )


class IngressBackend(BaseModel):
    resource: Optional[v1.TypedLocalObjectReference] = Field(
        None,
        description=(
            "resource is an ObjectRef to another Kubernetes resource in the namespace"
            " of the Ingress object. If resource is specified, a service.Name and"
            " service.Port must not be specified. This is a mutually exclusive setting"
            ' with "Service".'
        ),
    )
    service: Optional[IngressServiceBackend] = Field(
        None,
        description=(
            "service references a service as a backend. This is a mutually exclusive"
            ' setting with "Resource".'
        ),
    )


class IngressClass(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        None,
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ObjectMeta] = Field(
        None,
        description=(
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[IngressClassSpec] = Field(
        None,
        description=(
            "spec is the desired state of the IngressClass. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )


class IngressClassList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[IngressClass] = Field(
        ..., description="items is the list of IngressClasses."
    )
    kind: Optional[str] = Field(
        None,
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ListMeta] = Field(
        None, description="Standard list metadata."
    )


class NetworkPolicyPeer(BaseModel):
    ipBlock: Optional[IPBlock] = Field(
        None,
        description=(
            "ipBlock defines policy on a particular IPBlock. If this field is set then"
            " neither of the other fields can be."
        ),
    )
    namespaceSelector: Optional[v1_1.LabelSelector] = Field(
        None,
        description=(
            "namespaceSelector selects namespaces using cluster-scoped labels. This"
            " field follows standard label selector semantics; if present but empty, it"
            " selects all namespaces.\n\nIf podSelector is also set, then the"
            " NetworkPolicyPeer as a whole selects the pods matching podSelector in the"
            " namespaces selected by namespaceSelector. Otherwise it selects all pods"
            " in the namespaces selected by namespaceSelector."
        ),
    )
    podSelector: Optional[v1_1.LabelSelector] = Field(
        None,
        description=(
            "podSelector is a label selector which selects pods. This field follows"
            " standard label selector semantics; if present but empty, it selects all"
            " pods.\n\nIf namespaceSelector is also set, then the NetworkPolicyPeer as"
            " a whole selects the pods matching podSelector in the Namespaces selected"
            " by NamespaceSelector. Otherwise it selects the pods matching podSelector"
            " in the policy's own namespace."
        ),
    )


class NetworkPolicyStatus(BaseModel):
    conditions: Optional[List[v1_1.Condition]] = Field(
        None,
        description=(
            "conditions holds an array of metav1.Condition that describe the state of"
            " the NetworkPolicy. Current service state"
        ),
    )


class HTTPIngressPath(BaseModel):
    backend: IngressBackend = Field(
        ...,
        description=(
            "backend defines the referenced service endpoint to which the traffic will"
            " be forwarded to."
        ),
    )
    path: Optional[str] = Field(
        None,
        description=(
            "path is matched against the path of an incoming request. Currently it can"
            ' contain characters disallowed from the conventional "path" part of a URL'
            " as defined by RFC 3986. Paths must begin with a '/' and must be present"
            ' when using PathType with value "Exact" or "Prefix".'
        ),
    )
    pathType: str = Field(
        ...,
        description=(
            "pathType determines the interpretation of the path matching. PathType can"
            " be one of the following values: * Exact: Matches the URL path exactly. *"
            " Prefix: Matches based on a URL path prefix split by '/'. Matching is\n "
            " done on a path element by element basis. A path element refers is the\n "
            " list of labels in the path split by the '/' separator. A request is a\n "
            " match for path p if every p is an element-wise prefix of p of the\n "
            " request path. Note that if the last element of the path is a substring\n "
            " of the last element in request path, it is not a match (e.g. /foo/bar\n "
            " matches /foo/bar/baz, but does not match /foo/barbaz).\n*"
            " ImplementationSpecific: Interpretation of the Path matching is up to\n "
            " the IngressClass. Implementations can treat this as a separate PathType\n"
            "  or treat it identically to Prefix or Exact path types.\nImplementations"
            " are required to support all path types."
        ),
    )


class HTTPIngressRuleValue(BaseModel):
    paths: List[HTTPIngressPath] = Field(
        ..., description="paths is a collection of paths that map requests to backends."
    )


class IngressRule(BaseModel):
    host: Optional[str] = Field(
        None,
        description=(
            "host is the fully qualified domain name of a network host, as defined by"
            ' RFC 3986. Note the following deviations from the "host" part of the URI'
            " as defined in RFC 3986: 1. IPs are not allowed. Currently an"
            " IngressRuleValue can only apply to\n   the IP in the Spec of the parent"
            " Ingress.\n2. The `:` delimiter is not respected because ports are not"
            " allowed.\n\t  Currently the port of an Ingress is implicitly :80 for http"
            " and\n\t  :443 for https.\nBoth these may change in the future. Incoming"
            " requests are matched against the host before the IngressRuleValue. If the"
            " host is unspecified, the Ingress routes all traffic based on the"
            ' specified IngressRuleValue.\n\nhost can be "precise" which is a domain'
            ' name without the terminating dot of a network host (e.g. "foo.bar.com")'
            ' or "wildcard", which is a domain name prefixed with a single wildcard'
            " label (e.g. \"*.foo.com\"). The wildcard character '*' must appear by"
            " itself as the first DNS label and matches only a single label. You cannot"
            ' have a wildcard label by itself (e.g. Host == "*"). Requests will be'
            " matched against the Host field in the following way: 1. If host is"
            " precise, the request matches this rule if the http host header is equal"
            " to Host. 2. If host is a wildcard, then the request matches this rule if"
            " the http host header is to equal to the suffix (removing the first label)"
            " of the wildcard rule."
        ),
    )
    http: Optional[HTTPIngressRuleValue] = None


class IngressSpec(BaseModel):
    defaultBackend: Optional[IngressBackend] = Field(
        None,
        description=(
            "defaultBackend is the backend that should handle requests that don't match"
            " any rule. If Rules are not specified, DefaultBackend must be specified."
            " If DefaultBackend is not set, the handling of requests that do not match"
            " any of the rules will be up to the Ingress controller."
        ),
    )
    ingressClassName: Optional[str] = Field(
        None,
        description=(
            "ingressClassName is the name of an IngressClass cluster resource. Ingress"
            " controller implementations use this field to know whether they should be"
            " serving this Ingress resource, by a transitive connection (controller ->"
            " IngressClass -> Ingress resource). Although the"
            " `kubernetes.io/ingress.class` annotation (simple constant name) was never"
            " formally defined, it was widely supported by Ingress controllers to"
            " create a direct binding between Ingress controller and Ingress resources."
            " Newly created Ingress resources should prefer using the field. However,"
            " even though the annotation is officially deprecated, for backwards"
            " compatibility reasons, ingress controllers should still honor that"
            " annotation if present."
        ),
    )
    rules: Optional[List[IngressRule]] = Field(
        None,
        description=(
            "rules is a list of host rules used to configure the Ingress. If"
            " unspecified, or no rule matches, all traffic is sent to the default"
            " backend."
        ),
    )
    tls: Optional[List[IngressTLS]] = Field(
        None,
        description=(
            "tls represents the TLS configuration. Currently the Ingress only supports"
            " a single TLS port, 443. If multiple members of this list specify"
            " different hosts, they will be multiplexed on the same port according to"
            " the hostname specified through the SNI TLS extension, if the ingress"
            " controller fulfilling the ingress supports SNI."
        ),
    )


class NetworkPolicyEgressRule(BaseModel):
    ports: Optional[List[NetworkPolicyPort]] = Field(
        None,
        description=(
            "ports is a list of destination ports for outgoing traffic. Each item in"
            " this list is combined using a logical OR. If this field is empty or"
            " missing, this rule matches all ports (traffic not restricted by port). If"
            " this field is present and contains at least one item, then this rule"
            " allows traffic only if the traffic matches at least one port in the list."
        ),
    )
    to: Optional[List[NetworkPolicyPeer]] = Field(
        None,
        description=(
            "to is a list of destinations for outgoing traffic of pods selected for"
            " this rule. Items in this list are combined using a logical OR operation."
            " If this field is empty or missing, this rule matches all destinations"
            " (traffic not restricted by destination). If this field is present and"
            " contains at least one item, this rule allows traffic only if the traffic"
            " matches at least one item in the to list."
        ),
    )


class NetworkPolicyIngressRule(BaseModel):
    from_: Optional[List[NetworkPolicyPeer]] = Field(
        None,
        alias="from",
        description=(
            "from is a list of sources which should be able to access the pods selected"
            " for this rule. Items in this list are combined using a logical OR"
            " operation. If this field is empty or missing, this rule matches all"
            " sources (traffic not restricted by source). If this field is present and"
            " contains at least one item, this rule allows traffic only if the traffic"
            " matches at least one item in the from list."
        ),
    )
    ports: Optional[List[NetworkPolicyPort]] = Field(
        None,
        description=(
            "ports is a list of ports which should be made accessible on the pods"
            " selected for this rule. Each item in this list is combined using a"
            " logical OR. If this field is empty or missing, this rule matches all"
            " ports (traffic not restricted by port). If this field is present and"
            " contains at least one item, then this rule allows traffic only if the"
            " traffic matches at least one port in the list."
        ),
    )


class NetworkPolicySpec(BaseModel):
    egress: Optional[List[NetworkPolicyEgressRule]] = Field(
        None,
        description=(
            "egress is a list of egress rules to be applied to the selected pods."
            " Outgoing traffic is allowed if there are no NetworkPolicies selecting the"
            " pod (and cluster policy otherwise allows the traffic), OR if the traffic"
            " matches at least one egress rule across all of the NetworkPolicy objects"
            " whose podSelector matches the pod. If this field is empty then this"
            " NetworkPolicy limits all outgoing traffic (and serves solely to ensure"
            " that the pods it selects are isolated by default). This field is"
            " beta-level in 1.8"
        ),
    )
    ingress: Optional[List[NetworkPolicyIngressRule]] = Field(
        None,
        description=(
            "ingress is a list of ingress rules to be applied to the selected pods."
            " Traffic is allowed to a pod if there are no NetworkPolicies selecting the"
            " pod (and cluster policy otherwise allows the traffic), OR if the traffic"
            " source is the pod's local node, OR if the traffic matches at least one"
            " ingress rule across all of the NetworkPolicy objects whose podSelector"
            " matches the pod. If this field is empty then this NetworkPolicy does not"
            " allow any traffic (and serves solely to ensure that the pods it selects"
            " are isolated by default)"
        ),
    )
    podSelector: v1_1.LabelSelector = Field(
        ...,
        description=(
            "podSelector selects the pods to which this NetworkPolicy object applies."
            " The array of ingress rules is applied to any pods selected by this field."
            " Multiple network policies can select the same set of pods. In this case,"
            " the ingress rules for each are combined additively. This field is NOT"
            " optional and follows standard label selector semantics. An empty"
            " podSelector matches all pods in this namespace."
        ),
    )
    policyTypes: Optional[List[str]] = Field(
        None,
        description=(
            "policyTypes is a list of rule types that the NetworkPolicy relates to."
            ' Valid options are ["Ingress"], ["Egress"], or ["Ingress", "Egress"]. If'
            " this field is not specified, it will default based on the existence of"
            " ingress or egress rules; policies that contain an egress section are"
            " assumed to affect egress, and all policies (whether or not they contain"
            " an ingress section) are assumed to affect ingress. If you want to write"
            ' an egress-only policy, you must explicitly specify policyTypes [ "Egress"'
            " ]. Likewise, if you want to write a policy that specifies that no egress"
            ' is allowed, you must specify a policyTypes value that include "Egress"'
            " (since such a policy would not include an egress section and would"
            ' otherwise default to just [ "Ingress" ]). This field is beta-level in 1.8'
        ),
    )


class Ingress(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        None,
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ObjectMeta] = Field(
        None,
        description=(
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[IngressSpec] = Field(
        None,
        description=(
            "spec is the desired state of the Ingress. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )
    status: Optional[IngressStatus] = Field(
        None,
        description=(
            "status is the current state of the Ingress. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )


class IngressList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[Ingress] = Field(..., description="items is the list of Ingress.")
    kind: Optional[str] = Field(
        None,
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ListMeta] = Field(
        None,
        description=(
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )


class NetworkPolicy(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    kind: Optional[str] = Field(
        None,
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ObjectMeta] = Field(
        None,
        description=(
            "Standard object's metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
    spec: Optional[NetworkPolicySpec] = Field(
        None,
        description=(
            "spec represents the specification of the desired behavior for this"
            " NetworkPolicy."
        ),
    )
    status: Optional[NetworkPolicyStatus] = Field(
        None,
        description=(
            "status represents the current state of the NetworkPolicy. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status"
        ),
    )


class NetworkPolicyList(BaseModel):
    apiVersion: Optional[str] = Field(
        None,
        description=(
            "APIVersion defines the versioned schema of this representation of an"
            " object. Servers should convert recognized schemas to the latest internal"
            " value, and may reject unrecognized values. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources"
        ),
    )
    items: List[NetworkPolicy] = Field(
        ..., description="items is a list of schema objects."
    )
    kind: Optional[str] = Field(
        None,
        description=(
            "Kind is a string value representing the REST resource this object"
            " represents. Servers may infer this from the endpoint the client submits"
            " requests to. Cannot be updated. In CamelCase. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    )
    metadata: Optional[v1_1.ListMeta] = Field(
        None,
        description=(
            "Standard list metadata. More info:"
            " https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata"
        ),
    )
