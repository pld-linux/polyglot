Summary:	A compiler front end framework for building Java extensions
Summary(pl):	Szkielet frontendu kompilatora do tworzenia rozszerzeñ Javy
Name:		polyglot
%define	_pre	rc1
Version:	2.0
Release:	0.%{_pre}.1
License:	Apache v1.1
Group:		Development/Languages/Java
Source0:	http://www.cs.cornell.edu/Projects/polyglot/src/%{name}-%{version}%{_pre}-src.tar.gz
# Source0-md5:	5d87524f1b836467f47559e88e080f13
Patch0:		%{name}-classpath.patch
URL:		http://www.cs.cornell.edu/Projects/polyglot/src/
BuildRequires:	ant >= 1.6.5-4
BuildRequires:	jflex
BuildRequires:	jdk >= 1.3
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jre >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Polyglot is a highly extensible compiler front end for the Java
programming language. It is implemented as a Java class framework
using design patterns to promote extensibility. Using Polyglot,
language extensions can be implemented without duplicating code
from the framework itself. Polyglot has been used to implement
domain-specific languages, to explore language design ideas, to
simplify Java for pedagogical purposes, and for various code
transformations such as optimization and fault injection.
Polyglot has been used for both major and minor language extensions;
our experience suggests that the cost of implementing an extension
scales well with the degree to which it modifies Java.

%description -l pl
Polyglot to wysoce rozszerzalny frontend kompilatora dla jêzyka
programowania Java. Jest zaimplementowany jako szkielet klasy w Javie
przy u¿yciu szablonów projektowych promuj±cych rozszerzalno¶æ. Przy
u¿yciu Polyglota mo¿na implementowaæ rozszerzenia jêzyka bez
powielania kodu z samego szkieletu. Polyglot jest wykorzystywany do
implementowania jêzyków dla okre¶lonej dziedziny, badania idei
projektowych jêzyków, upraszczania Javy dla celów nauczania oraz do
ró¿nych przekszta³ceñ kodu, takich jak optymalizacja czy wstawianie
niepowodzeñ. Polyglot s³u¿y zarówno do du¿ych jak i nieznacznych
rozszerzeñ jêzyka; do¶wiadczenie sugeruje, ¿e koszt implementacji
rozszerzenia skaluje siê dobrze wraz ze stopniem modyfikacji Javy.

%prep
%setup -q -n %{name}-%{version}%{_pre}-src
%patch0 -p1

%build
required_jars='ant'
CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
export CLASSPATH="$CLASSPATH:`/usr/bin/build-classpath $required_jars`"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

%{ant} configure
%{ant} 
%{ant} javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir}/%{name},%{_bindir}}

sed -e "s|TOP=.*|TOP='%{_javadir}'|" bin/jlc > $RPM_BUILD_ROOT%{_bindir}/jlc
sed -e "s|TOP=.*|TOP='%{_javadir}'|" bin/pth > $RPM_BUILD_ROOT%{_bindir}/pth

install lib/{coffer,java_cup,pao,polyglot,pth}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/*
%{_javadir}/%{name}
