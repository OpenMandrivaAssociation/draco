%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

Summary:	Compress and decompres 3D geometric meshes and point clouds
Name:		draco
Version:	1.5.7
Release:	1
License:	Apache-2.0
URL:		https://github.com/google/%{name}
Source0:	https://github.com/google/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
# Downstream-only patch that unconditionally links a system copy of gtest,
# rather than expecting a git submodule as upstream prefers (and gtest upstream
# would recommend).
Patch0:		0001-Use-system-gtest.patch
# https://github.com/google/draco/pull/1001
Patch1:		0002-build-shared-lib.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	help2man
BuildRequires:	pkgconfig(python3)

%description
A library for compressing and decompressing 3D geometric meshes and point
clouds.

%files
%license LICENSE
%{_bindir}/%{name}_decoder*
%{_bindir}/%{name}_encoder*
%{_mandir}/man1/%{name}_decoder-%{version}.1*
%{_mandir}/man1/%{name}_encoder-%{version}.1*

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Compress and decompres 3D geometric meshes and point clouds
License:	Apache-2.0
Group:		System/Libraries

%description -n %{libname}
A library for compressing and decompressing 3D geometric meshes and point
clouds.


%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
License:	Apache-2.0
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%license LICENSE AUTHORS
%doc README.md
%{_includedir}/%{name}/
%{_datadir}/cmake/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# Remove precompiled CSS and Javascript along binaries
rm -fr {javascript,maya,docs/assets}

%build
%cmake \
    -DDRACO_TESTS:BOOL=OFF \
    -GNinja
%ninja_build


%install
%ninja_install -C build

# manpages
mkdir -p %{buildroot}%{_mandir}/man1
LD_LIBRARY_PATH=%{buildroot}%{_libdir} help2man -N --version-string=%{version} \
	-o %{buildroot}%{_mandir}/man1/%{name}_decoder-%{version}.1 \
	%{buildroot}%{_bindir}/%{name}_decoder
LD_LIBRARY_PATH=%{buildroot}%{_libdir} help2man -N --version-string=%{version} \
	-o %{buildroot}%{_mandir}/man1/%{name}_encoder-%{version}.1 \
	%{buildroot}%{_bindir}/%{name}_encoder

