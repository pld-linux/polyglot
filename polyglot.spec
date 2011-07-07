# 
# TODO:
#	- eclipse plugin is missing some files vital to packaging
#
Summary:	A compiler front end framework for building Java extensions
Summary(pl.UTF-8):	Szkielet frontendu kompilatora do tworzenia rozszerzeń Javy
Name:		polyglot
Version:	2.4.0
Release:	0.2
License:	Apache v1.1
Group:		Development/Languages/Java
Source0:	http://www.cs.cornell.edu/Projects/polyglot/src/%{name}-%{version}-src.tar.gz
# Source0-md5:	6a56a2a30ed3b164112a6caaddc6edb3
Source1:	http://www.cs.cornell.edu/Projects/polyglot/eclipseUpdates/plugins/%{name}_%{version}.jar
# Source1-md5:	c54716cc0412f08ce2a97e88934d064b
URL:		http://www.cs.cornell.edu/Projects/polyglot/
BuildRequires:	ant >= 1.6.5-4
BuildRequires:	jflex
BuildRequires:	jdk >= 1.3
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jre >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_eclipseplugindir	%{_libdir}/eclipse/dropins/%{name}

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

%package -n eclipse-polyglot
Summary:	Polyglot base compiler plugin for Eclipse
Summary(pl.UTF-8):	Wtyczka dla Eclipse z podstawowym kompilatorem Polyglot
Group:		Development/Languages
Requires:	eclipse >= 3.6

%description -n eclipse-polyglot
This plugin contains the Polyglot base compiler.
The plugin is made available to enable other plugins to extend
the Polyglot framework. No user-visible functionality is provided
by the Polyglot plugin itself. 

%description -n eclipse-polyglot -l pl.UTF-8
Ta wtyczka zawiera podstawowy kompilator Polyglot.
Wtyczka umożliwia innym wtyczkom rozszerzanie szkielet klas Polyglot.
Wtyczka nie udostępnia żadnej funkcjonalności widocznej dla
użytkownika.

%prep
%setup -q -n %{name}-%{version}-src

%build
required_jars='ant'
CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
export CLASSPATH="$CLASSPATH:`/usr/bin/build-classpath $required_jars`"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

%{ant} configure
%{ant} 
%{ant} jar
%{ant} examples
%{ant} jar-examples
%{ant} javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir}/%{name},%{_bindir}} \
	$RPM_BUILD_ROOT%{_eclipseplugindir}/features

sed -e "s|TOP=.*|TOP='%{_javadir}'|" bin/jlc > $RPM_BUILD_ROOT%{_bindir}/jlc
sed -e "s|TOP=.*|TOP='%{_javadir}'|" bin/pth > $RPM_BUILD_ROOT%{_bindir}/pth

install lib/{java_cup,polyglot,pth,ppg}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
install examples/coffer/lib/coffer.jar $RPM_BUILD_ROOT%{_javadir}/%{name}
install examples/pao/lib/pao.jar $RPM_BUILD_ROOT%{_javadir}/%{name}

install %{SOURCE1} $RPM_BUILD_ROOT%{_eclipseplugindir}/features

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_bindir}/*
%{_javadir}/%{name}

%if 0
%files -n eclipse-polyglot
%defattr(644,root,root,755)
%dir %{_eclipseplugindir}
%dir %{_eclipseplugindir}/features
%{_eclipseplugindir}/features/*
%endif
