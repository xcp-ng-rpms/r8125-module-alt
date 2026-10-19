%define vendor_name Realtek
%define vendor_label realtek
%define driver_name r8125

%if %undefined module_dir
%define module_dir extra
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{driver_name}-module-alt
Version: 9.018.00
Release: 1%{?dist}
License: GPL

# Origin: https://www.realtek.com/Download/List?cate_id=584
Source0: %{driver_name}-%{version}.tar.bz2

Patch0: 0001-config_change.patch
Patch1: 0002-use_new_api.patch
Patch2: 0003-txcsum_sg_tso_off.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/src INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Mon Oct 19 2026 Quentin Casasnovas <quentin.casasnovas@vates.tech> - 9.018.00-1
- Adding Realtek driver r8125 9.018.00 as r8125-module-alt
- Spec file and configuration based of the r8125-module package
