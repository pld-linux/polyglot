Summary:	A compiler front end framework for building Java extensions
Summary(pl.UTF-8):	Szkielet frontendu kompilatora do tworzenia rozszerzeń Javy
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

%description -l pl.UTF-8
Polyglot to wysoce rozszerzalny frontend kompilatora dla języka
programowania Java. Jest zaimplementowany jako szkielet klasy w Javie
przy użyciu szablonów projektowych promujących rozszerzalność. Przy
użyciu Polyglota można implementować rozszerzenia języka bez
powielania kodu z samego szkieletu. Polyglot jest wykorzystywany do
implementowania języków dla określonej dziedziny, badania idei
projektowych języków, upraszczania Javy dla celów nauczania oraz do
różnych przekształceń kodu, takich jak optymalizacja czy wstawianie
niepowodzeń. Polyglot służy zarówno do dużych jak i nieznacznych
rozszerzeń języka; doświadczenie sugeruje, że koszt implementacji
rozszerzenia skaluje się dobrze wraz ze stopniem modyfikacji Javy.

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
