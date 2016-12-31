import pytest
import pyecore.ecore as Ecore
from pyecore.resources import *
from pyecore.resources.xmi import XMIResource


def test_xmiresource_load_ecore_testEMF():
    global_registry[Ecore.nsURI] = Ecore
    resource = XMIResource(URI('tests/xmi/xmi-tests/testEMF.xmi'))
    resource.load()
    assert resource.contents != []
    root = resource.contents[0]
    A = root.getEClassifier('A')
    assert A
    B = root.getEClassifier('B')
    assert B
    TInterface = root.getEClassifier('TInterface')
    assert TInterface
    TClass = root.getEClassifier('TClass')
    assert TClass
    a = A()
    assert Ecore.EcoreUtils.isinstance(a, TClass)
    assert Ecore.EcoreUtils.isinstance(a, TInterface)
    assert A.findEStructuralFeature('abstract')
    assert A.findEStructuralFeature('isAbs')
    assert a.isAbs is False
    assert a.abstract is False


def test_resourceset_getresource_ecore_My():
    global_registry[Ecore.nsURI] = Ecore
    rset = ResourceSet()
    resource = rset.get_resource(URI('tests/xmi/xmi-tests/My.ecore'))
    assert resource.contents != []
    root = resource.contents[0]
    A = root.getEClassifier('A')
    B = root.getEClassifier('B')
    MyRoot = root.getEClassifier('MyRoot')
    assert A
    assert B
    assert MyRoot
    bRef = A.findEStructuralFeature('b')
    aRef = B.findEStructuralFeature('a')
    assert aRef.eOpposite is bRef


def test_resourceset_getresource_instance_MyRoot():
    global_registry[Ecore.nsURI] = Ecore
    rset = ResourceSet()
    # register the My.ecore metamodel in the resource set (could be in the global_registry)
    resource = rset.get_resource(URI('tests/xmi/xmi-tests/My.ecore'))
    root = resource.contents[0]
    rset.metamodel_registry[root.nsURI] = root
    # load the instance model
    resource = rset.get_resource(URI('tests/xmi/xmi-tests/MyRoot.xmi'))
    root = resource.contents[0]
    assert len(root.aContainer) == 2
    assert len(root.bContainer) == 1
    assert root.aContainer[0].b is root.bContainer[0]


def test_resourceset_getresource_ecore_Ecore():
     # load the ecore metamodel first
    global_registry[Ecore.nsURI] = Ecore
    rset = ResourceSet()
    resource = rset.get_resource(URI('tests/xmi/xmi-tests/Ecore.ecore'))
    root = resource.contents[0]
    assert root
    assert root.getEClassifier('EClass')
    assert root.getEClassifier('EAttribute')
    assert root.getEClassifier('EReference')
    assert root.getEClassifier('EPackage')


def test_resourceset_getresource_ecore_UML():
    global_registry[Ecore.nsURI] = Ecore
    rset = ResourceSet()
    # UMLPrimitiveTypes Creation
    umltypes = Ecore.EPackage('umltypes')
    String = Ecore.EDataType('String', str)
    Boolean = Ecore.EDataType('Boolean', bool, False)
    Integer = Ecore.EDataType('Integer', int, 0)
    UnlimitedNatural = Ecore.EDataType('UnlimitedNatural', int, 0)
    Real = Ecore.EDataType('Real', float, 0.0)
    umltypes.eClassifiers.extend([String, Boolean, Integer, UnlimitedNatural, Real])
    rset.resources['platform:/plugin/org.eclipse.uml2.types/model/Types.ecore'] = umltypes
    # Register Ecore metamodel instance
    resource = rset.get_resource(URI('tests/xmi/xmi-tests/Ecore.ecore'))
    rset.resources['platform:/plugin/org.eclipse.emf.ecore/model/Ecore.ecore'] = resource.contents[0]
    resource = rset.get_resource(URI('tests/xmi/xmi-tests/UML.ecore'))
    root = resource.contents[0]
    assert root.getEClassifier('Class')
    assert root.getEClassifier('Interface')
    assert root.getEClassifier('State')
