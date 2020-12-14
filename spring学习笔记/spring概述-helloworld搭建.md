# spring概述-helloworld搭建

## 简单了解框架

框架，即framework。其实就是某种应用的半成品，就是一组组件，供你选用完成你自己的系统。框架一般是成熟的，不断升级的软件。框架是对特定应用领域中的应用系统的部分设计和实现的整体结构。相当于别人帮你完成一些基础工作，你只需要完成系统业务逻辑设计。框架一般是成熟，稳健的，他可以处理系统很多细节问题，比如，事务处理，安全性，数据流控制等问题。

## spring概述

* Spring是一个开源框架
* Spring是一个**IOC**(DI)和**AOP**容器框架
* Spring为简化企业级开发而生，使用Spring，JavaBean就可以实现很多以前要靠EJB才能实现的功能。同样的功能，在EJB中要通过繁琐的配置和复杂的代码才能够实现，而在Spring中却非常的优雅和简洁。

## spring的优良特性：

* **非侵入式**：基于Spring开发的应用中的对象可以不依赖于Spring的API

* **依赖注入**：DI——Dependency Injection，反转控制(IOC)最经典的实现

* **面向切面编程**：Aspect Oriented Programming——AOP

* **容器**：Spring是一个容器，因为它包含并且管理应用对象的生命周期

* **组件化**：Spring实现了使用简单的组件配置组合成一个复杂的应用。在 Spring 中可以使用XML和Java注解组合这些对象。

* **一站式**：在IOC和AOP的基础上可以整合各种企业应用的开源框架和优秀的第三方类库（实际上Spring 自身也提供了表述层的SpringMVC和持久层的Spring JDBC）。

  ![](image\spring结构图.png)

## 搭建运行环境

1. 建立动态web工程

2. 导包

   1. Spring自身JAR包（spring-beans、spring-context、spring-core、spring-expression）
   2. commons-logging包

3. 创建spring配置文件（xml文件）

   1) 在Spring Tool Suite工具中通过如下步骤创建Spring的配置文件

   ​	① File->New->Spring Bean Configuration File（New下没有这个选择就点击other，然后查出来）

   ​	② 为文件取名字 例如：applicationContext.xml

对于配置文件的编写：

```xml
<!-- 
  <bean>:定义spring所管理的一个对象
  id:该对象的唯一标示，注意：不能重复，在通过类型获取bean的过程中可以不设置
  class:此对象所属类的全限定名
  -->
<bean id="personOne" class="com.atguigu.spring.mod.Person">
    <!-- 
   <property>:为对象的某个属性赋值
   name:属性名
   value:属性值
   -->
    <property name="id" value="1111"></property>
    <property name="name" value="小明"></property>
</bean>
```

手动获取创建的spring管理的对象：

```java
//初始化容器
ApplicationContext ac = new ClassPathXmlApplicationContext("applicationContext.xml");
//通过getBean()获取对象
//Person person = (Person)ac.getBean("person");
//使用此方法获取对象时，要求spring所管理的此类型的对象只能有一个
//Person person = ac.getBean(Person.class);
Person person = ac.getBean("personOne", Person.class);
System.out.println(person);
```

